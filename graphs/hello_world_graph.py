from typing import Dict, TypedDict
from langgraph.graph import StateGraph 

class AgentState(TypedDict):
    name: str
    message: str

def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state."""
    
    state["message"] = "Hey " + state["name"] + ", how is your day going?"

    return state

def compliment_node(state: AgentState) -> AgentState:
    """Simple node that compliments a person."""

    state["message"] += " You are doing amazing " + state["name"]

    return state

graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)
graph.add_node("compliment", compliment_node)

graph.set_entry_point("greeter")
graph.add_edge("greeter", "compliment")
graph.set_finish_point("compliment")

app = graph.compile()

print(app.invoke({"name": "Santosh", "message": ""}))
