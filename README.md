# Agentic AI for DevOps

A hands-on learning and portfolio project exploring Python, LLMs, AI agents, retrieval-augmented generation (RAG), Model Context Protocol (MCP), and multi-agent systems for practical DevOps troubleshooting.

## Objectives

- Build a strong foundation in Python and LLM concepts.
- Develop agents that investigate CI/CD and infrastructure failures.
- Retrieve known solutions from a troubleshooting knowledge base.
- Explore MCP tools and multi-agent workflows.
- Apply tests, auditability, and human approval before changes.
- Prepare for Agentic AI and DevOps interviews with practical examples.

## Repository Structure

| Directory | Purpose |
|---|---|
| `01-python-fundamentals/` | Python basics and first log analyzer |
| `02-llm-fundamentals/` | Prompting and LLM concepts |
| `03-ai-agents/` | Agent decision flow and human approval |
| `04-rag/` | Starter knowledge retrieval; later embeddings and vector search |
| `05-mcp/` | Model Context Protocol learning module |
| `06-multi-agent-systems/` | Separate investigation and recommendation roles |
| `07-devops-ai-project/` | Practical log analyzer and tests |
| `interview-preparation/` | Interview questions, answers, and revision notes |

## Getting Started

Requirements: Python 3.10+ recommended, Git, and optionally Visual Studio Code.

Run the first exercise from the repository root:

```powershell
python .\01-python-fundamentals\agent.py
```

Run the project tests:

```powershell
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

## Safety Principles

- Analyze logs before proposing a fix.
- Require explicit human approval before making changes.
- Do not expose API keys, passwords, tokens, kubeconfig files, or sensitive production logs.
- Test proposed changes before production deployment.

## Learning Status

- [x] Rule-based timeout and null-pointer detection
- [ ] LLM-powered troubleshooting
- [ ] Agent tool calling
- [ ] RAG with embeddings and a vector store
- [ ] MCP server and client
- [ ] Multi-agent orchestration
- [ ] End-to-end DevOps AI project

This repository will evolve as each module is studied, implemented, tested, and documented. Starter examples in this initial commit are educational demonstrations; rule-based functions are not yet full LLM-powered agents.