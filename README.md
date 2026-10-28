# Agentic AI for DevOps — From Python Basics to Your Own Agents

![Cloud-native engineering](https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?auto=format&fit=crop&w=1600&q=85)

**Learn by building:** Python → AI agents → RAG → MCP → multi-agent systems → DevOps troubleshooting → Kubernetes SRE automation patterns.

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
| [08 — K-Agent](08-k-agent/README.md) | Kubernetes health inventory, warning events and logs, known-remedy guidance, exact human approval before supported restarts, and unit tests |
| [09 — Advanced SRE Agent](09-advanced-sre-agent/README.md) | Incident correlation, evidence-first diagnosis, runbook RAG roadmap, approval/policy gates, post-change verification, and architecture diagram |

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

## Additional hands-on examples

Each learning folder now has another focused example alongside its existing starter code:

- [Environment check](00-environment-setup/environment_check.py)
- [Python DevOps metrics](01-python-fundamentals/devops_metrics_example.py)
- [Prompt patterns](02-llm-fundamentals/prompt_patterns.py)
- [Bounded agent loop](03-ai-agents/bounded_agent_loop.py)
- [RAG metadata filtering](04-rag/metadata_filter_retrieval.py)
- [MCP synthetic health tool](05-mcp/mcp_health_server.py)
- [Multi-agent pipeline](06-multi-agent-systems/multi_agent_pipeline_example.py)
- [Multi-line incident triage](07-devops-ai-project/incident_triage_example.py)
- [Interview scenario drills](interview-preparation/scenario_drills.py)

Each module README links to its additional example and explains how to run it or what to expect. The MCP server example requires the MCP SDK and an MCP-compatible client; it uses synthetic data and does not contact real infrastructure.

## 08 — K-Agent: Kubernetes health and troubleshooting

[Open the K-Agent module](08-k-agent/README.md) — Kubernetes resource inventory, Pod logs and warning-event analysis, conservative known-solution guidance, exact human approval before supported workload restarts, and unit tests. This is an educational first version; CRD instances and every API type are not automatically understood, and live-cluster testing is still required.


## 09 — Advanced SRE Agent

![Advanced SRE architecture](09-advanced-sre-agent/assets/advanced-sre-agent-architecture.svg)

Explore the [advanced SRE module](09-advanced-sre-agent/README.md), run the [offline incident correlator](09-advanced-sre-agent/incident_correlator.py), and follow its [line-by-line code walkthrough](09-advanced-sre-agent/CODE_WALKTHROUGH.md). This adds an evidence-correlation example and a roadmap for metrics, timelines, runbook retrieval, audit controls, approval-gated remediation, and post-change verification.

**Visuals and project honesty:** photos in the README are externally hosted image links; the architecture diagram above is a local SVG committed in this repository. Advanced SRE integrations are clearly marked as future work until implemented and tested.
