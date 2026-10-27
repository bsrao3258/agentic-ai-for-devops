# Agentic AI for DevOps

A hands-on learning and portfolio project exploring Python, LLMs, AI agents, retrieval-augmented generation (RAG), Model Context Protocol (MCP), and multi-agent systems for practical DevOps troubleshooting.

## Learning Path

Follow the folders in numerical order:

| Order | Directory | Purpose |
|---|---|---|
| 00 | [Environment Setup](00-environment-setup/README.md) | Prepare Python `.venv` on Windows/Linux and connect it to VS Code |
| 01 | [Python Fundamentals](01-python-fundamentals/README.md) | Python basics and first log analyzer |
| 02 | [LLM Fundamentals](02-llm-fundamentals/README.md) | Prompting and LLM concepts |
| 03 | [AI Agents](03-ai-agents/README.md) | Agent decision flow and human approval |
| 04 | [RAG](04-rag/README.md) | Starter knowledge retrieval; later embeddings and vector search |
| 05 | [MCP](05-mcp/README.md) | Model Context Protocol learning module |
| 06 | [Multi-Agent Systems](06-multi-agent-systems/README.md) | Separate investigation and recommendation roles |
| 07 | [DevOps AI Project](07-devops-ai-project/README.md) | Practical log analyzer and tests |
| — | [Interview Preparation](interview-preparation/README.md) | Interview questions, answers, and revision notes |

## Quick Start

First, follow the complete [Environment Setup guide](00-environment-setup/README.md). It covers Windows PowerShell, Linux, creating and activating a virtual environment, selecting the interpreter in VS Code, and running the starter exercises.

After cloning the repository and creating your environment, run these commands from the repository root.

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

## Objectives

- Build a strong foundation in Python and LLM concepts.
- Develop agents that investigate CI/CD and infrastructure failures.
- Retrieve known solutions from a troubleshooting knowledge base.
- Explore MCP tools and multi-agent workflows.
- Apply tests, auditability, and human approval before changes.
- Prepare for Agentic AI and DevOps interviews with practical examples.

## Safety Principles

- Analyze logs before proposing a fix.
- Require explicit human approval before making changes.
- Do not expose API keys, passwords, tokens, kubeconfig files, or sensitive production logs.
- Test proposed changes before production deployment.
- Keep `.venv` and local secrets out of Git; see [`.gitignore`](.gitignore).

## Learning Status

- [x] Initial rule-based timeout and null-pointer detection
- [x] Local environment setup guide for Windows, Linux, and VS Code
- [ ] LLM-powered troubleshooting
- [ ] Agent tool calling
- [ ] RAG with embeddings and a vector store
- [ ] MCP server and client
- [ ] Multi-agent orchestration
- [ ] End-to-end DevOps AI project

This repository will evolve as each module is studied, implemented, tested, and documented. Starter examples are educational demonstrations; rule-based functions are not yet full LLM-powered agents.
