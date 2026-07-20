# lalalangraph

A small [LangGraph](https://github.com/langchain-ai/langgraph) sandbox for learning how to build stateful, node-based graphs.

## What it does

[hello_world.py](hello_world.py) builds a minimal two-node graph that greets and compliments a person:

```
greeter → compliment
```

State flows through an `AgentState` dict carrying a `name` and a `message`. Each node reads the name and appends to the message:

- **greeter** — builds the greeting from `name`
- **compliment** — appends a compliment, also from `name`

Running it produces:

```
{'name': 'Santosh', 'message': 'Hey Santosh, how is your day going? You are doing amazing Santosh'}
```

## Requirements

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) for dependency management

## Setup

```bash
uv sync
```

## Run

```bash
uv run python hello_world.py
```
