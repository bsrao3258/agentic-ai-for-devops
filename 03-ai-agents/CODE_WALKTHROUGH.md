# AI Agents — Line-by-Line Code Walkthrough

## Example 1: Read-only local tool

```python
def inspect_log(logs: str) -> dict:
    text = logs.lower()
    return {
        "timeout": "timeout" in text,
        "null_pointer": "null pointer" in text,
        "evidence": logs.strip(),
    }
```

- `def inspect_log(...)` defines a function that examines a supplied log.
- `logs: str` is a type hint indicating expected text input.
- `-> dict` indicates the function is intended to return a dictionary.
- `logs.lower()` normalizes letter case for matching.
- The dictionary groups related results under named keys.
- `"timeout" in text` produces `True` if that phrase occurs, otherwise `False`.
- `logs.strip()` removes whitespace from the beginning and end; it does not remove internal spaces.
- This function is a local helper. A model has not selected or called it automatically.

## Example 2: Approval decision

```python
def propose_action(action: str, approved: bool) -> str:
    if not approved:
        return f"Approval required before: {action}"
    return f"Approved for execution: {action}"
```

- `action: str` is the proposed action text.
- `approved: bool` represents a Boolean approval flag.
- `if not approved:` checks whether approval is false.
- The first `return` produces a message and exits the function when approval is absent.
- The final `return` is reached only if `approved` is true.
- This is a teaching example, not a secure approval system. A production system must verify the approver and bind approval to the exact target and action, and the executor must enforce authorization independently.

## Agent concepts
A genuine LLM-powered agent typically receives a goal, uses a model to choose among permitted tools, observes tool results, updates context, and stops when complete or when it needs help. A robust implementation also needs tool schemas, bounded steps, timeouts, error handling, and audit logs.

## Practice
Add a `disk full` detector. Then write tests that verify the tool returns the correct result and that no infrastructure-changing function is called.
