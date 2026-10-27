# 07 — End-to-End DevOps Troubleshooting Project

## Goal
Build an assistant that analyzes sanitized CI/CD logs, identifies known patterns, explains evidence, consults approved runbooks, recommends safe checks, and requests explicit approval before remediation.

## Current capabilities
- Rule-based timeout, null-pointer, and unknown classification.
- Recommendation mapping.
- Unit tests for classification.
- Additional sample incident-report script in `examples.py`.

These examples do not connect to Jenkins, Kubernetes, cloud APIs, or production systems.

## Run from repository root

Windows PowerShell:
```powershell
python .\07-devops-ai-project\log_analyzer.py
python .\07-devops-ai-project\examples.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

Linux:
```bash
python ./07-devops-ai-project/log_analyzer.py
python ./07-devops-ai-project/examples.py
python -m unittest discover -s ./07-devops-ai-project/tests -v
```

## Sample output: log analyzer
```text
Error type: TIMEOUT
Recommendation: Check network connectivity, latency, and server health.
Approval required before applying any fix.
```

## Sample output: incident report
```text
Category: TIMEOUT
Evidence: The log contains the word 'timeout'.
Next steps:
- Check server health
- Check network latency
- Review retry settings
Approval required: True
```

## Architecture roadmap
1. **Input:** sanitized CI/CD logs.
2. **Classifier:** identify known patterns and preserve evidence.
3. **Retriever:** find approved, relevant runbooks.
4. **LLM layer (future):** summarize evidence, list hypotheses, cite sources.
5. **Tools (future):** read-only Jenkins/Kubernetes/MCP queries with strict schemas.
6. **Approval gate:** show exact action and target; require explicit approval.
7. **Executor (future):** perform only allowlisted approved actions in a sandbox.
8. **Audit and tests:** record redacted evidence, decision, approval, outcome, and test results.

## Roadmap
- [x] Deterministic classifier
- [x] Basic unit tests
- [x] Structured incident report example
- [ ] Sanitized file input and robust error handling
- [ ] Runbook retrieval and source references
- [ ] LLM integration with schema validation
- [ ] Read-only MCP tools
- [ ] Human-approved remediation in a sandbox
- [ ] CI checks and security review

## Production safety
Never pipe raw model output into a shell. Never let a model choose arbitrary commands, namespaces, clusters, or credentials. Validate and authorize every action independently of model output. Start read-only and test outside production.
