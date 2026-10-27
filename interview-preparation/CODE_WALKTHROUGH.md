# Interview Preparation — How to Explain the Code

Use these explanations as a starting point, then practice explaining them without reading.

## Explain the classifier
1. The function accepts a log string as input.
2. It normalizes the text to lowercase so matching is case-insensitive.
3. It checks known patterns in order.
4. It returns a category at the first match.
5. It returns `UNKNOWN` when no configured pattern matches.
6. A separate function maps each category to a suggested next step.
7. Unit tests check known examples and prevent regressions.

## Explain why return is useful
`return` sends a value to the caller so another function can use it. `print` is for displaying text. Returning a structured result makes code easier to test, reuse, and connect to a UI or an LLM.

## Explain the agent roadmap honestly
The current rule-based classifier is not a full autonomous agent. The planned evolution is: sanitized input → classification and evidence → approved runbook retrieval → LLM summary → validated read-only tool calls → human approval → narrowly scoped execution → audit trail.

## Explain human approval
The system should show the exact proposed action, target, evidence, risk, and expected impact. Approval should be recorded for that specific proposal, and a separate executor must enforce permissions. A prompt or printed approval message is not enough.

## Practice question
**Interviewer:** What happens if the agent cannot identify a known error?
**Good answer structure:** It should report uncertainty, preserve the relevant evidence, request additional diagnostics or a human review, and avoid guessing or applying a fix automatically.
