"""Prompt-design examples. These examples do not call an LLM API."""


def prompt_for_ci_failure(logs: str) -> str:
    return (
        "Role: cautious DevOps troubleshooting assistant\n"
        "Task: analyze the sanitized CI log.\n"
        "Return: observed evidence, likely causes, read-only checks, uncertainty.\n"
        "Safety: do not execute commands or claim actions were performed.\n"
        f"Log:\n{logs}"
    )


def prompt_for_kubernetes_event(event: str) -> str:
    return (
        "Explain this Kubernetes event for a junior engineer. "
        "Separate facts from hypotheses and propose read-only checks only.\n"
        f"Event: {event}"
    )


if __name__ == "__main__":
    print(prompt_for_ci_failure("Jenkins failed: connection timeout"))
    print("\n--- SECOND EXAMPLE ---")
    print(prompt_for_kubernetes_event("Pod entered CrashLoopBackOff"))
