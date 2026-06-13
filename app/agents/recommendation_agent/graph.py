from langgraph.graph import StateGraph, END, START
from app.agents.recommendation_agent.state import RecommendationState
from app.agents.recommendation_agent.nodes import (
    fetch_users_recent_completed_songs,
    fetch_users_recent_liked_songs,
    fetch_users_recent_skipped_songs,
    create_summary_completed_song,
    create_summary_liked_song,
    create_summary_skipped_song,
    summarize_liked_skipped_completed_summary
)

def build_graph():
    graph = StateGraph(RecommendationState)

    # register nodes
    graph.add_node("completed_songs", fetch_users_recent_completed_songs)
    graph.add_node("liked_songs", fetch_users_recent_liked_songs)
    graph.add_node("skipped_songs", fetch_users_recent_skipped_songs)
    graph.add_node("summary_completed_song", create_summary_completed_song)
    graph.add_node("summary_liked_songs", create_summary_liked_song)
    graph.add_node("summary_skipped_songs", create_summary_skipped_song)
    graph.add_node("summary_liked_skipped_completed", summarize_liked_skipped_completed_summary)


    # define flow
    graph.add_edge(START,"completed_songs")
    graph.add_edge(START,"liked_songs")
    graph.add_edge(START,"skipped_songs")
    graph.add_edge("completed_songs", "summary_completed_song")
    graph.add_edge("liked_songs", "summary_liked_songs")
    graph.add_edge("skipped_songs", "summary_skipped_songs")
    graph.add_edge("summary_completed_song", "summary_liked_skipped_completed")
    graph.add_edge("summary_liked_songs", "summary_liked_skipped_completed")
    graph.add_edge("summary_skipped_songs", "summary_liked_skipped_completed")
    graph.add_edge("summary_liked_skipped_completed",END)


    return graph.compile()

recommendation_graph = build_graph()