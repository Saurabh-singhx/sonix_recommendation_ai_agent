from typing import TypedDict, List, Optional

class RecommendationState(TypedDict):
    user_id: str
    liked_songs: List[int]
    skipped_songs: List[str]  
    completed_songs: List[str]

    liked_songs_summary:str
    skipped_songs_summary:str
    completed_songs_summary:str

    summary_liked_skipped_completed:str

    user_ai_summary:str
    
    recommendation_summary:str
    recommendation_songs: List[str]

    error: Optional[str]