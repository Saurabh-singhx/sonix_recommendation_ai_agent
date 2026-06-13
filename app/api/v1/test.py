from fastapi import APIRouter
from app.agents.test_agents.graph import recommendation_graph

router = APIRouter()

@router.post("/test/{user_id}/refresh")
async def refresh(user_id: str):
    initial_state = {
        "user_id": user_id,
        "play_history": [],
        "candidate_songs": [],
        "recommendations": [],
        "error": None
    }
    result = await recommendation_graph.ainvoke(initial_state)
    return {"recommendations": result["recommendations"]}