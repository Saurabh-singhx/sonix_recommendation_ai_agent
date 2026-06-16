from app.agents.recommendation_agent.state import RecommendationState
from langchain_core.messages import HumanMessage
from app.core.database import db
from app.core.llm import llm
import logging
from functools import wraps
from pydantic import BaseModel
from langchain_core.messages import AIMessage
from app.agents.recommendation_agent.tools import (
    get_users_recent_liked_songs,
    get_users_recent_skipped_songs,
    get_user_recent_completed_songs,
    
    get_all_artist_name,     #tools for ai
    get_most_repeated_song,
    get_song_by_genre,
    get_songs_by_energy_level,
    get_songs_by_likes,
    get_songs_by_mood,
    get_songs_by_tags,
    get_todays_trending_song,
)

reommendation_tools_for_ai = [ get_all_artist_name,
    get_most_repeated_song,
    get_song_by_genre,
    get_songs_by_energy_level,
    get_songs_by_likes,
    get_songs_by_mood,
    get_songs_by_tags,
    get_todays_trending_song,]

logger = logging.getLogger(__name__)

def node_error_handler(fallback: dict):
    def decorator(func):
        @wraps(func)
        async def wrapper(state):
            try:
                return await func(state)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                return {**fallback, "error": f"{func.__name__} failed: {e}"}
        return wrapper
    return decorator

@node_error_handler(fallback={"liked_songs": []})
async def fetch_users_recent_liked_songs(state:RecommendationState) -> RecommendationState:

    recent_liked_songs = await get_users_recent_liked_songs.ainvoke(state["user_id"])

    return {"liked_songs": recent_liked_songs}

@node_error_handler(fallback={"skipped_songs": []})
async def fetch_users_recent_skipped_songs(state:RecommendationState) -> RecommendationState:

    recent_skipped_songs = await get_users_recent_skipped_songs.ainvoke(state["user_id"])

    return {"skipped_songs": recent_skipped_songs}

@node_error_handler(fallback={"completed_songs": []})
async def fetch_users_recent_completed_songs(state:RecommendationState) -> RecommendationState:

    recent_completed_songs = await get_user_recent_completed_songs.ainvoke(state["user_id"])

    return {"completed_songs": recent_completed_songs}

@node_error_handler(fallback={"liked_songs_summary": ""})
async def create_summary_liked_song(state:RecommendationState) -> RecommendationState:

    response = await llm.ainvoke(
        f"User recently liked these songs: {state['liked_songs']}. "
        f"summarize this in detail so other recommendation ai can recommend songs easily"
        f"Return summarize text"
    )
    
    content = response.content
    if isinstance(content, str):
        pass 
    elif isinstance(content, list):
        content = next((b.get("text", "") for b in content if b.get("type") == "text"), "")

    return {"liked_songs_summary": content}

@node_error_handler(fallback={"skipped_songs_summary": ""})
async def create_summary_skipped_song(state:RecommendationState) -> RecommendationState:

    response = await llm.ainvoke(
        f"User recently skipped these songs: {state['skipped_songs']}. "
        f"summarize this in detail so other recommendation ai can recommend songs easily"
        f"Return summarize text"
    )
    
    content = response.content
    if isinstance(content, str):
        pass 
    elif isinstance(content, list):
        content = next((b.get("text", "") for b in content if b.get("type") == "text"), "")

    return {"skipped_songs_summary": content}

@node_error_handler(fallback={"completed_songs_summary": ""})
async def create_summary_completed_song(state:RecommendationState) -> RecommendationState:

    response = await llm.ainvoke(
        f"User recently completed these songs: {state['completed_songs']}. "
        f"summarize this in detail so other recommendation ai can recommend songs easily"
        f"Return summarize text"
    )
    
    content = response.content
    if isinstance(content, str):
        pass 
    elif isinstance(content, list):
        content = next((b.get("text", "") for b in content if b.get("type") == "text"), "")

    return {"completed_songs_summary": content}

@node_error_handler(fallback={"summary_liked_skipped_completed": ""})
async def summarize_liked_skipped_completed_summary(state:RecommendationState) -> RecommendationState:

    response = await llm.ainvoke(
        f"after careful analysing these summaries: {state['completed_songs_summary'],state['liked_songs_summary'],state['skipped_songs_summary']}. "
        f"summarize this in detail so other recommendation ai can recommend songs easily"
        f"Return summarize text"
    )
    
    content = response.content
    if isinstance(content, str):
        pass 
    elif isinstance(content, list):
        content = next((b.get("text", "") for b in content if b.get("type") == "text"), "")

    return {"summary_liked_skipped_completed": content}


llm_with_tools = llm.bind_tools(reommendation_tools_for_ai)

@node_error_handler(fallback={"messages": []})
async def recommendation_agent_node(state: RecommendationState) -> RecommendationState:
    if not state["messages"]:
        prompt = (
            f"User profile summary: {state['summary_liked_skipped_completed']}. "
            f"Use the available tools to fetch candidate songs that match this user's taste, "
            f"then recommend 50 songs with reasoning."
            f"give only song_id and song name"
        )
        human_message = HumanMessage(content=prompt)
        response = await llm_with_tools.ainvoke([human_message])
        return {"messages": [human_message, response]}

    response = await llm_with_tools.ainvoke(state["messages"])

    return {"messages": [response]}

class RecommendedSong(BaseModel):
    song_id: str
    song_name: str

class RecommendationOutput(BaseModel):
    songs: list[RecommendedSong]
    summary: str

def get_last_ai_message(state: RecommendationState) -> AIMessage | None:
    for message in reversed(state["messages"]):
        if isinstance(message, AIMessage):
            return message
    return None

structured_llm = llm.with_structured_output(RecommendationOutput)

@node_error_handler(fallback={"recommendation_summary":"","recommendation_songs":[]})
async def final_recommendation_node(state: RecommendationState) -> RecommendationState:
    message = get_last_ai_message(state)

    response = await structured_llm.ainvoke(
        f"extract song_id and summary for next song recommendation from this message {message}"
    )
    print(response.songs)
    print(response.summary)
    
    return {"recommendation_summary":response.summary,"recommendation_songs":response.songs}
