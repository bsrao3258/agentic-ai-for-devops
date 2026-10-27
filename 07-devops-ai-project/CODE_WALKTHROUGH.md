# DevOps AI Project — Line-by-Line Code Walkthrough

## Incident report function

```python
def analyze_incident(logs: str) -> dict:
    text = logs.lower()
    if "timeout" in text:
        category = "TIMEOUT"
        evidence = "The log contains the word 'timeout'."
        next_steps = ["Check server health", "Check network latency", "Review retry settings"]
    elif "null pointer" in text:
        category = "NULL_POINTER"
        evidence = "The log contains the phrase 'null pointer'."
        next_steps = ["Inspect the stack trace", "Check variable initialization", "Review recent changes"]
    else:
        category = "UNKNOWN"
        evidence = "No configured error pattern matched."
        next_steps = ["Collect surrounding logs", "Check recent deployments", "Consult an approved runbook"]

    return {
        "category": category,
        "evidence": evidence,
        "next_steps": next_steps,
        "approval_required_before_changes": True,
    }
```

- The function accepts log text and promises to return a dictionary.
- `logs.lower()` makes matching case-insensitive.
- The `if` branch detects a timeout pattern and assigns a category, an evidence explanation, and a list of investigation steps.
- The `elif` branch does the same for null-pointer errors, but only if the timeout condition was false.
- The `else` branch provides a conservative fallback when neither pattern matches.
- `next_steps` is a list so the caller can display or process each suggestion separately.
- The returned dictionary groups the incident fields into one structured report.
- `approval_required_before_changes: True` communicates the intended safety rule. This flag alone does not enforce approval or execute a remediation.

## Main block
- `if __name__ == "__main__":` prevents the demonstration from running automatically when imported.
- The sample string simulates a Jenkins timeout log.
- `analyze_incident(...)` creates the report.
- The print statements display each field.
- The `for step in report["next_steps"]:` loop prints each recommended check on its own line.

Expected output:
```text
Category: TIMEOUT
Evidence: The log contains the word 'timeout'.
Next steps:
- Check server health
- Check network latency
- Review retry settings
Approval required: True
```

## Important limitation
This is a deterministic rules-based example. It does not call an LLM, retrieve live runbooks, connect to Jenkins/Kubernetes, or apply fixes. A future production design should redact secrets, cite evidence, use read-only tools first, validate every proposed action, and enforce approval outside the model.

## Practice
Add a category for `permission denied`, add unit tests, and make sure unknown errors never trigger a remediation automatically.
