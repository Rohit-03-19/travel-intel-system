from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.researcher import researcher_node
from app.core.logging import logger

# 1. Define placeholder nodes for Phase 1
def planner_node(state: AgentState):
    logger.info("--- ENTERING PLANNER AGENT ---")
    return {"itinerary": {"Day 1": "Visit Temple"}, "next_step": END}

# 2. Build the Workflow
workflow = StateGraph(AgentState)

# Nodes add karo
workflow.add_node("researcher", researcher_node)
workflow.add_node("planner", planner_node)

# Flow set karo (Edges)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "planner")
workflow.add_edge("planner", END)

# Compile karo (Ye hum main.py mein use karenge)
travel_agent_app = workflow.compile()