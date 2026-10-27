"""Deterministic examples of agent building blocks."""


def inspect_log(logs: str) -> dict:
    text = logs.lower()
    return {
        "timeout": "timeout" in text,
        "null_pointer": "null pointer" in text,
        "evidence": logs.strip(),
    }


def propose_action(action: str, approved: bool) -> str:
    if not approved:
        return f"Approval required before: {action}"
    return f"Approved for execution: {action}"


if __name__ == "__main__":
    print(inspect_log("Jenkins connection timeout"))
    print(propose_action("restart staging service", approved=False))
