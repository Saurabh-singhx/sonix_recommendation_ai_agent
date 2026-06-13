from langgraph.graph import StateGraph, END
from app.agents.test_agents.state import RecommendationState
from app.agents.test_agents.nodes import (
    fetch_history,
    generate_candidates,
    save_recommendations,
)

def build_graph():
    graph = StateGraph(RecommendationState)

    # register nodes
    graph.add_node("fetch_history", fetch_history)
    graph.add_node("generate_candidates", generate_candidates)
    graph.add_node("save_recommendations", save_recommendations)

    # define flow
    graph.set_entry_point("fetch_history")
    graph.add_edge("fetch_history", "generate_candidates")
    graph.add_edge("generate_candidates", "save_recommendations")
    graph.add_edge("save_recommendations", END)

    return graph.compile()

recommendation_graph = build_graph()