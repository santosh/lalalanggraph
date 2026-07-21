from langgraph.graph import StateGraph, END
import random
from typing import TypedDict, Literal, NotRequired


class AgentState(TypedDict):
    name: str
    message: NotRequired[str]
    number: list[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""

    state["message"] = f"Hi there, {state['name']}!"
    state["counter"] = 0

    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10."""

    state["number"] = state["number"] + [random.randint(0, 10)]
    state["counter"] += 1

    return state

def should_continue(state: AgentState) -> Literal["loop", "exit"]:
    """Function to decide what to do next"""

    if state["counter"] < 5:
        print("Entering loop", state["counter"])
        return "loop"
    else:
        return "exit"

def main():
    graph = StateGraph(AgentState)

    graph.add_node("greeting", greeting_node)
    graph.add_node("random", random_node)

    graph.add_edge("greeting", "random")

    graph.add_conditional_edges(
        "random",
        should_continue,
        {
            "loop": "random",
            "exit": END
        }
    )

    graph.set_entry_point("greeting")

    app = graph.compile()

    print(app.invoke({"name": "Santosh", "number": [], "counter": 0}))


if __name__ == "__main__":
    main()
