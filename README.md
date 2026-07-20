# lalalangraph

A small [LangGraph](https://github.com/langchain-ai/langgraph) sandbox for learning how to build stateful, node-based graphs.

## Getting started

Requirements:

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) for dependency management

Install dependencies:

```bash
uv sync
```

## Examples

Each script is a self-contained graph you can run with `uv run python <file>`.

### hello_world.py

A two-node graph that greets and compliments a person:

```
greeter → compliment
```

State flows through an `AgentState` dict carrying a `name` and a `message`. `greeter` builds the greeting from `name`, and `compliment` appends a compliment from the same `name`.

```bash
uv run python hello_world.py
# {'name': 'Santosh', 'message': 'Hey Santosh, how is your day going? You are doing amazing Santosh'}
```

### multiple_inputs.py

A single node that reads several fields off the state at once — a list of `values`, a `name`, and an `operation`:

```
processor
```

The `processor` node sums (`+`) or multiplies (`*`) the list and writes a personalized `result`.

```bash
uv run python multiple_inputs.py
# {'values': [12, 21, 33], 'name': 'Santosh', 'operation': '*', 'result': 'Hi there Santosh! Your answer is: 8316'}
```
