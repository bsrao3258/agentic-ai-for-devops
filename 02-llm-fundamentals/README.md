# 02 — LLM Fundamentals

## Learning goals
Understand what an LLM does, how prompts influence output, why responses can be wrong, and how to validate answers before using them in DevOps.

## 1. What is an LLM?
A large language model predicts and generates text based on its learned patterns and current context. It does not automatically know your live infrastructure, and it can produce plausible but incorrect answers.

## 2. Build a prompt

```python
def build_prompt(logs):
    return f"""You are a cautious DevOps assistant.
Analyze the sanitized log below.
Return: likely issue, evidence, safe read-only checks, and uncertainty.
Do not claim to have run commands. Do not apply fixes.
LOG:
{logs}
"""

print(build_prompt("Jenkins: connection timeout"))
```
Expected output begins with `You are a cautious DevOps assistant.` and includes the supplied log. This prints a prompt; it does not call a model.

## 3. Prompting examples
- Weak: "Fix this."
- Better: "Analyze this sanitized Jenkins timeout. List evidence, likely causes, read-only checks, and what remains uncertain. Do not change systems."
- For structured output, request fields such as `summary`, `evidence`, `checks`, and `confidence`; validate the result in Python rather than trusting free text blindly.

## 4. Token/context and hallucinations
Models have context limits. Very long logs should be filtered, summarized carefully, or retrieved in relevant chunks. A hallucination is a generated claim that is not supported by evidence. Ask the model to distinguish observed log facts from hypotheses.

## 5. Safe integration pattern
1. Remove secrets and personal data from logs.
2. Send only the necessary context to an approved model endpoint.
3. Validate the returned schema and allowed actions.
4. Show the recommendation to the user.
5. Require human approval before changes.

## Exercises
1. Add a prompt for a Kubernetes CrashLoopBackOff.
2. Ask for evidence separately from hypotheses.
3. Define a JSON schema for a recommendation.
4. List three cases where the model should say it does not know.

## Interview questions
- What is an LLM and what are its limitations?
- What is a token and context window?
- How do you reduce hallucinations?
- Why should model output be validated?
- What sensitive data must not be sent in logs?
