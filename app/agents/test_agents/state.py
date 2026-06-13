from typing import TypedDict, List, Optional

class RecommendationState(TypedDict):
    user_id: str
    play_history: List[int]       # song ids user has played
    candidate_songs: List[str]    # songs to consider
    recommendations: List[str]    # final output
    error: Optional[str]