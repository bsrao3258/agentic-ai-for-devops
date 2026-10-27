# 07 — DevOps AI Troubleshooting Project

## Goal
Build toward an assistant that analyzes CI/CD logs, identifies known issues, consults troubleshooting knowledge, recommends a fix, and requests explicit human approval before making changes.

## Current implementation
- Rule-based error classification
- Recommendations for timeout and null-pointer patterns
- Unknown-error fallback
- Unit tests for classification

## Run
From the repository root:

```powershell
python .\07-devops-ai-project\log_analyzer.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

## Safety
This starter only analyzes sample text and prints recommendations. It does not connect to Jenkins, Kubernetes, or production systems and does not apply fixes.

## Planned enhancements
1. Read sanitized log files.
2. Add structured findings and confidence.
3. Retrieve approved runbook steps.
4. Add an LLM with output validation.
5. Add read-only DevOps tools through MCP.
6. Add an approval gate, audit trail, and controlled execution.
