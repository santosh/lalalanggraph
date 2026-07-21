from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    operation: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    
    output = 0
    if state["operation"] == "*":
        # Multiply all values
        output = 1
        for value in state["values"]:
            output *= value
    elif state["operation"] == "+":
        # Sum all values
        output = sum(state["values"])


    state['result'] = f"Hi there {state['name']}! Your answer is: {output}"

    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

def main():
    print(app.invoke({"name": "Santosh", "values": [12, 21, 33], "operation": "*", "result": ""}))

if __name__ == "__main__":
    main()
