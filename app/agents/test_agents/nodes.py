from app.agents.test_agents.state import RecommendationState
from app.core.database import db
from app.core.llm import llm

async def fetch_history(state: RecommendationState) -> RecommendationState:
    """Node 1: fetch what user has played"""
    plays = await db.song_suggestion.find_many(
        take=50
    )
    return {**state, "play_history": [p.song_id for p in plays]}

async def generate_candidates(state: RecommendationState) -> RecommendationState:
    """Node 2: ask Gemini to pick candidates"""
    response = await llm.ainvoke(
        f"User has played song ids: {state['play_history']}. "
        f"Suggest 10 similar song ids from the library. "
        f"Return only a comma separated list of ids."
    )
    
    # response.content is a list of blocks, get the text from first block
    content = response.content
    if isinstance(content, list):
        content = content[0].get("text", "") if isinstance(content[0], dict) else content[0]

    ids = [x.strip() for x in content.split(",")]
    return {**state, "candidate_songs": ids}

async def save_recommendations(state: RecommendationState) -> RecommendationState:
    """Node 3: delete old and save new recommendations"""
    # await db.recommendation.delete_many(
    #     where={"userId": state["user_id"]}
    # )
    # await db.recommendation.create_many(data=[
    #     {"userId": state["user_id"], "songId": sid}
    #     for sid in state["candidate_songs"]
    # ])
    return {**state, "recommendations": state["candidate_songs"]}