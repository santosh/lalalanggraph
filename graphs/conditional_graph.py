from typing import TypedDict, Literal, NotRequired
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int
    operation1: str
    number2: int
    finalNumber1: NotRequired[int]
    number3: int
    operation2: str
    number4: int
    finalNumber2: NotRequired[int]


def adder1(state: AgentState) -> AgentState:
    """This node adds the 2 numbers."""

    state["finalNumber1"] = state["number1"] + state["number2"]
    return state

def subtractor1(state: AgentState) -> AgentState:
    """This node subtracts the 2 numbers."""

    state["finalNumber1"] = state["number1"] - state["number2"]
    return state

def adder2(state: AgentState) -> AgentState:
    """This node adds the 2 numbers."""

    state["finalNumber2"] = state["number3"] + state["number4"]
    return state

def subtractor2(state: AgentState) -> AgentState:
    """This node subtracts the 2 numbers."""

    state["finalNumber2"] = state["number3"] - state["number4"]
    return state


def decide_first_operation(state: AgentState) -> Literal["addition_operation", "subtraction_operation"]:
    """This node will select the next node of the graph."""

    if state["operation1"] == "+":
        return "addition_operation"
    if state["operation1"] == "-":
        return "subtraction_operation"

    raise ValueError(f"Unsupported operation: {state['operation1']!r}")


def decide_second_operation(state: AgentState) -> Literal["addition_operation", "subtraction_operation"]:
    """This node will select the next node of the graph."""

    if state["operation2"] == "+":
        return "addition_operation"
    if state["operation2"] == "-":
        return "subtraction_operation"

    raise ValueError(f"Unsupported operation: {state['operation2']!r}")


graph = StateGraph(AgentState)

graph.add_node("router1", lambda state: state)
graph.add_node("add_node1", adder1)
graph.add_node("subtract_node1", subtractor1)

graph.add_edge(START, "router1")

graph.add_conditional_edges(
    "router1",
    decide_first_operation,
    {
        "addition_operation": "add_node1",
        "subtraction_operation": "subtract_node1"
    },
)

graph.add_edge("add_node1", "router2")
graph.add_edge("subtract_node1", "router2")

graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtractor2)
graph.add_node("router2", lambda state: state)

graph.add_conditional_edges(
    "router2",
    decide_second_operation,
    {
        "addition_operation": "add_node2",
        "subtraction_operation": "subtract_node2"
    },
)

graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

app = graph.compile()

if __name__ == "__main__":
    initial_state_1 = AgentState(number1=10, operation1="-", number2=5, number3=20, operation2="-", number4=10)
    initial_state_2 = AgentState(number1=10, operation1="+", number2=5, number3=20, operation2="+", number4=10)
    initial_state_3 = AgentState(number1=10, operation1="+", number2=5, number3=20, operation2="-", number4=10)
    print(app.invoke(initial_state_1))
    print(app.invoke(initial_state_2))
    print(app.invoke(initial_state_3))
