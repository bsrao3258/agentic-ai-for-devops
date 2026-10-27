# Agentic AI for DevOps — From Python Basics to Your Own Agents

A hands-on, beginner-friendly course and portfolio. Each module includes concepts, runnable examples, expected output, exercises, and interview questions. Work through the modules in numerical order.

## Learning path

| Module | What you will build |
|---|---|
| [00 — Environment Setup](00-environment-setup/README.md) | Python, virtual environments, VS Code, and Git on Windows/Linux |
| [01 — Python Fundamentals](01-python-fundamentals/README.md) | Variables, strings, collections, conditions, loops, functions, files, exceptions, and tests |
| [02 — LLM Fundamentals](02-llm-fundamentals/README.md) | Prompt design, structured outputs, model limits, and safe LLM integration concepts |
| [03 — AI Agents](03-ai-agents/README.md) | Agent loop, tools, state, approval gates, and error handling |
| [04 — RAG](04-rag/README.md) | Knowledge ingestion, retrieval, grounding, and a path to vector search |
| [05 — MCP](05-mcp/README.md) | MCP client/server concepts and a local tool server |
| [06 — Multi-Agent Systems](06-multi-agent-systems/README.md) | Specialist roles, handoffs, coordination, and failure handling |
| [07 — End-to-End DevOps Project](07-devops-ai-project/README.md) | A tested log-troubleshooting assistant with safety controls |
| [Interview Preparation](interview-preparation/README.md) | Concept questions, scenario questions, and project storytelling |

## Prerequisites

- Python 3.10+ (Python 3.11+ recommended for newer AI libraries)
- Git
- VS Code and the Microsoft Python extension
- An internet connection for installing optional dependencies

Start with [the environment setup guide](00-environment-setup/README.md). Do not commit `.venv`, credentials, API keys, kubeconfig files, or real production logs.

## Run the first examples

From the repository root, with the virtual environment activated:

### Windows PowerShell
```powershell
python .\01-python-fundamentals\agent.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

### Linux
```bash
python ./01-python-fundamentals/agent.py
python -m unittest discover -s ./07-devops-ai-project/tests -v
```

Module READMEs include sample outputs. Outputs are examples of what the code should print; actual model responses may vary when a live LLM is introduced.

## Important distinction

A Python script using `if/elif/else` is a rule-based program, not automatically an AI agent. This course builds the foundation first, then introduces LLMs, tool use, retrieval, MCP, and orchestration. Do not describe a demo as production-ready or claim production experience you have not gained.

## Safety model for DevOps agents

1. Start with read-only diagnostics and sanitized logs.
2. Show the evidence and proposed action in plain language.
3. Ask for explicit human approval before a state-changing action.
4. Validate inputs, scope credentials narrowly, and record an audit trail.
5. Test in a sandbox before production.

## Suggested study routine

For each lesson: read the concept, type the code yourself, run it, compare output, change one thing, complete the exercise, and write a short explanation in your own words. Use the interview module to revise. This is an evolving educational repository; dependencies and advanced modules will be added as they are implemented and tested.
