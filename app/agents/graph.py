from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.agents.nodes.researcher import researcher_node
from app.agents.nodes.planner import planner_node 
from app.agents.nodes.concierge import concierge_node
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# 1. StateGraph Initialize
workflow = StateGraph(AgentState)

# 2. Nodes Add Karo
workflow.add_node("researcher", researcher_node)
workflow.add_node("planner", planner_node)
workflow.add_node("concierge", concierge_node)

# 3. Connections (Edges) - Modern START/END Flow
# Safar shuru: START -> Researcher
workflow.add_edge(START, "researcher")

# Researcher -> Planner (Yahan interrupt lagega compilation ke waqt)
workflow.add_edge("researcher", "planner")

# Planner -> Concierge
workflow.add_edge("planner", "concierge")

# Concierge -> END (Safar khatam)
workflow.add_edge("concierge", END)

# 4. Persistence & Compilation
# Checkpoint DB connection (Ye AI ki 'Pause' state save karega)
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# Graph ko Compile karo with Interrupt
travel_agent_app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["planner"] # Planner node chalne se pehle execution ruk jayegi
)