from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    skills: list[str]
    final: str


def first_node(state: AgentState) -> AgentState:
    """This is first node of our sequence"""

    state["final"] = f"Hi {state["name"]}."
    return state

def second_node(state: AgentState) -> AgentState:
    """This is second node of our sequence"""

    state["final"] += f" You are {state["age"]} years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """This is third node of our sequence"""

    state["final"] += f" You are skilled in {', '.join(state['skills'])}."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"name": "Charlie", "age": 20, "skills": ["Python", "TDD"], "final": ""})

    print(result)
