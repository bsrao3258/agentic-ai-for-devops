# Agentic AI for DevOps — From Python Basics to Your Own Agents

A hands-on, beginner-friendly course and portfolio. Each module includes concepts, runnable examples, expected output, exercises, and interview questions. Work through the modules in numerical order.

## Learning path

| Module | What you will build |
|---|---|
| [00 — Environment Setup](00-environment-setup/README.md) | Python, virtual environments, VS Code, and Git on Windows/Linux |
| [01 — Python Fundamentals](01-python-fundamentals/README.md) | Variables, strings, collections, conditions, loops, functions, files, exceptions, and tests |
| [02 — LLM Fundamentals](02-llm-fundamentals/README.md) | Prompt design, model limits, and safe LLM integration concepts |
| [03 — AI Agents](03-ai-agents/README.md) | Agent loop, tools, state, approval gates, and error handling |
| [04 — RAG](04-rag/README.md) | Knowledge ingestion, retrieval, grounding, and vector-search concepts |
| [05 — MCP](05-mcp/README.md) | MCP client/server concepts and a local tool server |
| [06 — Multi-Agent Systems](06-multi-agent-systems/README.md) | Specialist roles, handoffs, coordination, and failure handling |
| [07 — End-to-End DevOps Project](07-devops-ai-project/README.md) | Tested log troubleshooting assistant with safety controls |
| [Interview Preparation](interview-preparation/README.md) | Concept and scenario questions |

## Start here

Follow [Environment Setup](00-environment-setup/README.md) first. It covers Windows PowerShell, Linux, creating and activating a virtual environment, selecting the interpreter in VS Code, and running tests.

With the environment active, from the repository root:

**Windows PowerShell**
```powershell
python .\01-python-fundamentals\agent.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

**Linux**
```bash
python ./01-python-fundamentals/agent.py
python -m unittest discover -s ./07-devops-ai-project/tests -v
```

## Safety principles

- Start with sanitized logs and read-only diagnostics.
- Separate observed evidence from hypotheses.
- Require explicit human approval before state-changing actions.
- Validate tool inputs and scope credentials with least privilege.
- Never pass arbitrary model output to a shell.
- Never commit API keys, passwords, tokens, kubeconfig files, or sensitive production logs.

## Learning status

- [x] Rule-based log classification and starter tests
- [x] Environment setup guide
- [ ] LLM-powered troubleshooting
- [ ] Agent tool calling
- [ ] RAG with embeddings and a vector store
- [ ] MCP client/server integration
- [ ] Multi-agent orchestration
- [ ] End-to-end sandboxed remediation

**Important:** A script using `if/elif/else` is a useful rule-based program, but it is not automatically an LLM-powered agent. This course builds foundations first, then adds model reasoning, retrieval, tools, and orchestration. Examples are educational and not production-ready by default.
