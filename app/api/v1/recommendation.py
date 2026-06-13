from fastapi import APIRouter
from app.agents.recommendation_agent.graph import recommendation_graph

router = APIRouter()

@router.post("/recommendation/{user_id}/refresh")
async def refresh(user_id: str):
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

        "error": None
    }
    result = await recommendation_graph.ainvoke(initial_state)
    return {"summary_liked_skipped_completed": result["summary_liked_skipped_completed"]}
