from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """This is an addition function that adds 2 numbers together."""

    return a + b

@tool
def subtract(a: int, b: int):
    """This is a subtraction function that subtract one number from other."""

    return a - b

@tool
def multiply(a: int, b: int):
    """This is an multiplication function that multiplies 2 numbers together."""

    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI assistant, please answer my query to the best of your ability.")

    # ensure messages sequence is converted to a list before concatenation
    response = model.invoke([system_prompt] + list(state["messages"]))

    return {"messages": [response]}

def should_continue(state: AgentState):
    message = state["messages"]
    last_message = message[-1]
    if not getattr(last_message, "tool_calls", None):
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs: AgentState = {
    "messages": [
        HumanMessage(
            content="Add 40 + 12 and then multiply the results by 6.And also tell me a joke please?"
        )
    ]
}
print_stream(app.stream(inputs, stream_mode="values"))
