# Multi-Agent Systems — Line-by-Line Code Walkthrough

## How the example works
The example contains three ordinary Python functions that represent separate responsibilities. They are not yet LLM-powered agents.

### 1. Investigator
- `def investigator_agent(logs: str) -> dict:` defines a function that accepts logs and returns a dictionary.
- `logs.lower()` normalizes case.
- The timeout and null-pointer conditions check for known phrases.
- Each matched branch returns a finding plus the evidence phrase that triggered it.
- The fallback records that no known pattern matched rather than inventing a cause.

### 2. Runbook researcher
- `def runbook_agent(finding: dict) -> str:` accepts the investigator's result.
- It checks the `evidence` field to select a relevant safe next step.
- The returned string is the handoff result. A real retriever would search approved runbooks and return source references.

### 3. Reviewer
- `def reviewer_agent(finding, recommendation)` accepts both the finding and proposed next step.
- `supported = ...` checks whether a known pattern matched.
- The returned dictionary combines the finding, recommendation, support flag, and approval reminder.
- The flag is a simple demonstration; production review requires stronger validation and evidence checks.

### 4. Orchestration
- The `if __name__ == "__main__":` block runs the demonstration only when executed directly.
- The investigator runs first; its result is passed to the runbook function.
- The recommendation and finding are passed to the reviewer.
- `print` statements display the final handoff and status.

Expected output:
```text
Investigation: Likely network or server timeout.
Recommendation: Check network path and server health.
Status: Approval required before any remediation.
```

## Why use multiple roles?
Separate roles can improve organization, but they also add latency, cost, and failure modes. Use multiple agents only when specialization provides a measurable benefit. Add maximum handoff counts, timeouts, structured messages, and a clear stop condition.

## Practice
Add a runbook researcher that returns a source ID. Make the reviewer reject any recommendation without evidence, then write tests for that rule.
