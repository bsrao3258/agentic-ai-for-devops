# 03 — Build Your First DevOps Agent

## What is an agent?
An AI agent typically combines a goal, model-driven reasoning, state/context, and tools that can observe or act on an environment. A fixed `if/elif` script is useful groundwork but is not by itself a full LLM-powered agent.

## 1. Start with a deterministic workflow
The existing `devops_agent.py` classifies a log and prints a recommendation. It does not call an LLM or change infrastructure.

## 2. Agent loop concept
A common controlled loop is: receive task → inspect evidence → choose an allowed tool → validate result → update state → stop or ask for help. Put maximum step limits and timeouts around loops.

## 3. Tool example (safe local function)

```python
def inspect_log(logs):
    """A local read-only tool over supplied text."""
    return {"contains_timeout": "timeout" in logs.lower()}

result = inspect_log("Jenkins connection timeout")
print(result)
```
Expected output: `{'contains_timeout': True}`

A real agent could choose this tool through model tool-calling, but the function itself is not an LLM agent.

## 4. Approval gate example

```python
def propose_action(action: str, approved: bool) -> str:
    if not approved:
        return f"Approval required before: {action}"
    return f"Approved for execution: {action}"

print(propose_action("restart staging service", approved=False))
```
Expected output: `Approval required before: restart staging service`

In production, approval must be tied to the exact action, target, parameters, identity, and expiration. A printed message is not a security control.

## 5. Design rules
- Start with read-only tools.
- Use allowlists and validate arguments.
- Never expose unrestricted shell access to a model.
- Require approval for restarts, deployments, rollbacks, or other state changes.
- Log tool name, arguments (redacted), result, approver, and timestamp.
- Set timeouts, retry limits, and a maximum number of agent steps.

## Exercises
1. Add a disk-space classification.
2. Return structured dictionaries rather than printing.
3. Add an approval function and test both approved and rejected cases.
4. Define a maximum of three tool calls.
5. Explain what the agent must do when no known solution is found.

## Interview questions
- How is an agent different from a chatbot or rule-based script?
- What is a tool call?
- How do you prevent an agent from taking dangerous actions?
- Why are timeouts and step limits important?
