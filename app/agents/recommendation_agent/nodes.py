from app.agents.recommendation_agent.state import RecommendationState
from app.core.database import db
from app.core.llm import llm
from app.agents.recommendation_agent.tools import (
    get_users_recent_liked_songs,
    get_users_recent_skipped_songs,
    get_user_recent_completed_songs
)

async def fetch_users_recent_liked_songs(state:RecommendationState) -> RecommendationState:

    recent_liked_songs = await get_users_recent_liked_songs.ainvoke(state["user_id"])

    return {"liked_songs": recent_liked_songs}

async def fetch_users_recent_skipped_songs(state:RecommendationState) -> RecommendationState:

    recent_skipped_songs = await get_users_recent_skipped_songs.ainvoke(state["user_id"])

    return {"skipped_songs": recent_skipped_songs}

async def fetch_users_recent_completed_songs(state:RecommendationState) -> RecommendationState:

    recent_completed_songs = await get_user_recent_completed_songs.ainvoke(state["user_id"])

    return {"completed_songs": recent_completed_songs}

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