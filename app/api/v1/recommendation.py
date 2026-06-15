from fastapi import APIRouter,HTTPException
from app.agents.recommendation_agent.graph import recommendation_graph

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/recommendation/{user_id}/refresh")
async def refresh(user_id: str):
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="user_id is required")
     
    initial_state = {
        "user_id": user_id,
        "liked_songs": [],
        "skipped_songs": [],
        "completed_songs": [],

        "liked_songs_summary":"",
        "skipped_songs_summary":"",
        "completed_songs_summary":"",

        "summary_liked_skipped_completed":"",

        "user_ai_summary":"",

        "recommendation_summary":"",
        "recommendation_songs":[],
        "messages": [],
        "error": None
    }
    try:
        result = await recommendation_graph.ainvoke(initial_state)
    except Exception as e:
        logger.error(f"recommendation_graph failed for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

    if result.get("error"):
        logger.warning(f"Partial failure for user {user_id}: {result['error']}")

    return {"result":result.get("messages")}
