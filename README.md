# Agentic AI for DevOps — From Python Basics to Your Own Agents

A hands-on, beginner-friendly course and portfolio. The goal is to take a learner from **core Python** to building and understanding **LLM-powered agents, RAG, MCP, multi-agent systems, and a DevOps troubleshooting project**. Each module should include explanations, runnable examples, expected output, exercises, and interview questions.

## Start here

1. [00 — Environment Setup](00-environment-setup/README.md) — install Python/Git, create a virtual environment, and configure VS Code.
2. [01 — Python Fundamentals](01-python-fundamentals/README.md) — start with the fundamentals; do not skip this module.
   - [Full Core Python Curriculum](01-python-fundamentals/CORE_PYTHON_CURRICULUM.md) — plain-English explanations, multiple examples per concept, expected outputs, exercises, and interview questions.
   - [Runnable Python examples](01-python-fundamentals/examples_with_output.py) — run the examples in your terminal.
3. [Screenshots and Diagrams](docs/SCREENSHOTS_AND_DIAGRAMS.md) — learning-flow diagrams and a checklist for capturing genuine environment/setup screenshots.

## Complete learning path

| Module | What you will learn/build |
|---|---|
| [00 — Environment Setup](00-environment-setup/README.md) | Python, virtual environments, VS Code, and Git on Windows/Linux |
| [01 — Python Fundamentals](01-python-fundamentals/README.md) | Variables, types, operators, strings, collections, conditions, loops, functions, modules, files, exceptions, classes, JSON, environment variables, and tests |
| [02 — LLM Fundamentals](02-llm-fundamentals/README.md) | Prompts, tokens/context, model limits, and safe LLM integration concepts |
| [03 — AI Agents](03-ai-agents/README.md) | Agent loop, tools, state, approval gates, and error handling |
| [04 — RAG](04-rag/README.md) | Knowledge ingestion, retrieval, grounding, and vector-search concepts |
| [05 — MCP](05-mcp/README.md) | MCP client/server concepts and a local tool server |
| [06 — Multi-Agent Systems](06-multi-agent-systems/README.md) | Specialist roles, handoffs, coordination, and failure handling |
| [07 — End-to-End DevOps Project](07-devops-ai-project/README.md) | Tested log troubleshooting assistant with safety controls |
| [Interview Preparation](interview-preparation/README.md) | Core Python, LLM, agent, RAG, MCP, multi-agent, and DevOps scenario questions |

## Run your first examples

From the repository root:

**Windows PowerShell**
```powershell
python .\01-python-fundamentals\examples_with_output.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

**Linux**
```bash
python ./01-python-fundamentals/examples_with_output.py
python -m unittest discover -s ./07-devops-ai-project/tests -v
```

Compare the terminal output with the examples in the curriculum. The exact display of filesystem paths may differ between Windows and Linux.

## Diagrams and screenshots

GitHub renders the Mermaid diagrams in [Screenshots and Diagrams](docs/SCREENSHOTS_AND_DIAGRAMS.md). That guide also lists the actual screenshots a learner can capture locally for Python version checks, virtual-environment activation, VS Code interpreter selection, example execution, and test results. Screenshots should reflect a real setup and must not expose secrets or production data.

## Safety principles

- Start with sanitized logs and read-only diagnostics.
- Separate observed evidence from hypotheses.
- Require explicit human approval before state-changing actions.
- Validate tool inputs and scope credentials with least privilege.
- Never pass arbitrary model output to a shell.
- Never commit API keys, passwords, tokens, kubeconfig files, or sensitive production logs.

## Project maturity and honest boundaries

The current examples are primarily educational, deterministic Python examples. A script using `if/elif/else` is a useful rule-based program, but it is not automatically an LLM-powered agent. The RAG starter demonstrates retrieval concepts rather than a full production vector database, and the multi-agent starter illustrates role separation rather than guaranteeing independent LLM reasoning. Full LLM integration, production-grade retrieval, secure tool execution, and end-to-end sandboxed remediation require further implementation and testing.

## Suggested learner workflow

For every concept: **read → predict output → run → compare → modify → explain**. Complete the exercises and interview questions before moving on. Always ask for human approval before a system changes infrastructure or production state.
