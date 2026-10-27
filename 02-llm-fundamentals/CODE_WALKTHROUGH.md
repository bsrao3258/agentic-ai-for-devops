# LLM Fundamentals — Line-by-Line Code Walkthrough

The examples in this folder build prompts only. They do **not** send a request to an LLM provider.

## Example: Build a prompt

```python
def build_prompt(logs):
    return f"""You are a cautious DevOps assistant.
Analyze the sanitized log. Return observed evidence, likely causes,
safe read-only checks, and uncertainty. Do not execute commands.
LOG:
{logs}
"""

print(build_prompt("Jenkins: connection timeout"))
```

Line by line:
- `def build_prompt(logs):` defines a function that accepts a log string.
- `return` sends the completed prompt back to the caller.
- The `f` before the triple quotes enables an f-string, so expressions inside braces are replaced by their values.
- Triple quotes allow a multi-line string.
- The role and task instructions tell a future model what kind of response is wanted.
- “Observed evidence” asks for facts from the log; “likely causes” asks for hypotheses. Keeping these separate reduces confusion.
- “Safe read-only checks” requests investigation steps that should not change infrastructure.
- `{logs}` inserts the supplied log into the prompt.
- `print(...)` displays the generated text. It does not invoke an LLM API.

## Example: CI failure prompt

In `examples.py`:
- `def prompt_for_ci_failure(logs: str) -> str:` defines a function. `: str` and `-> str` are type hints for readers and tools; Python does not enforce them at runtime.
- Parenthesized adjacent string literals are concatenated by Python.
- `\n` inserts a newline so the prompt is readable.
- `f"Log:\n{logs}"` inserts the supplied log after the label.
- The final `if __name__ == "__main__":` block runs examples only when the file is executed directly.
- The second function frames a Kubernetes event for a junior engineer and requests facts, hypotheses, and read-only checks.

## What is still missing for a real LLM call?
A real integration needs a provider/client library, securely configured credentials, network request, error handling, timeout, response parsing, and output validation. Never hardcode API keys or send secrets in logs. Model output must be treated as untrusted data.

## Practice
1. Add a line asking the model to state when evidence is insufficient.
2. Add a request for structured fields: `summary`, `evidence`, and `next_checks`.
3. Explain why printing a prompt is not the same as calling a model.
