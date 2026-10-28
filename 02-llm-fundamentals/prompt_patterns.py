"""Example 2: build prompts for two different DevOps tasks.

No LLM API is called; this script only builds and prints prompt text.
"""


def build_incident_prompt(service: str, logs: str) -> str:
    return (
        "Task: summarize this incident for an on-call engineer.\n"
        "Rules: separate facts from hypotheses; do not invent telemetry; "
        "recommend read-only checks only.\n"
        f"Service: {service}\nSanitized logs:\n{logs}"
    )


def build_json_prompt(question: str) -> str:
    return (
        "Answer using exactly these JSON fields: summary, evidence, "
        "safe_checks, uncertainty. Do not include markdown.\n"
        f"Question: {question}"
    )


if __name__ == "__main__":
    print(build_incident_prompt("payments-api", "HTTP 503 from upstream"))
    print("\n--- STRUCTURED OUTPUT PROMPT ---")
    print(build_json_prompt("Why might an upstream request return HTTP 503?"))
