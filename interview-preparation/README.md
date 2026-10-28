# Interview Preparation — Agentic AI for DevOps

Use this as a revision checklist. Practice answers aloud in your own words and connect them to repository code. Do not claim production experience or metrics you have not achieved.

## Python
1. Explain functions, parameters, return values, collections, exceptions, and modules.
2. What is the difference between `print` and `return`?
3. How would you unit-test a log classifier?
4. How do virtual environments and dependency files improve reproducibility?

## LLMs
1. What is an LLM? What are tokens and context windows?
2. What are hallucinations, and how do you reduce their impact?
3. How do you validate structured output?
4. What log data should be redacted before model use?

## Agents and tools
1. What makes an agent different from a fixed rule-based program?
2. Explain the observe/decide/tool/result loop.
3. How do you limit tool access and prevent arbitrary shell execution?
4. When must an agent ask for human approval?

## RAG
1. Explain ingestion, chunking, embeddings, retrieval, generation, and citations.
2. How do you evaluate retrieval relevance?
3. What is the difference between RAG and fine-tuning?
4. How do you defend against instructions embedded in retrieved documents?

## MCP
1. Explain MCP host, client, server, tools, and resources.
2. Why use a standard protocol instead of bespoke integrations?
3. How do you secure tool inputs, credentials, and outputs?
4. Which operations should remain read-only?

## Multi-agent systems
1. When does multi-agent orchestration add value?
2. How do agents hand off state?
3. How do you stop loops and handle contradictory results?
4. What are latency, cost, and reliability trade-offs?

## DevOps scenarios
1. A Jenkins pipeline times out. What evidence do you gather first?
2. A Kubernetes pod restarts repeatedly. Which read-only checks are safe?
3. A proposed fix is known but could affect production. How do you get approval?
4. How do you audit a recommendation and remediation?

## Project storytelling
Use this structure: problem → constraints → architecture → implementation → tests → safety → limitations → next steps. Distinguish completed functionality from planned work.

## Practice task
Explain how this repository progresses from a keyword-based Python classifier to an LLM-powered agent that uses approved runbooks and read-only MCP tools. Explicitly state which components are currently implemented and which remain future work.

## Additional example: scenario drills

Run from the repository root:

```powershell
python .\interview-preparation\scenario_drills.py
```

Linux:

```bash
python ./interview-preparation/scenario_drills.py
```

The script prints two interview scenarios and short answer outlines: troubleshooting a Jenkins timeout and explaining why a rule-based classifier is not automatically an AI agent. Practice answering each question aloud in your own words before reviewing the outline.

[Open the scenario-drill code](scenario_drills.py).
