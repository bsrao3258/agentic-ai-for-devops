"""A small end-to-end rule-based incident report example."""


def analyze_incident(logs: str) -> dict:
    text = logs.lower()
    if "timeout" in text:
        category = "TIMEOUT"
        evidence = "The log contains the word 'timeout'."
        next_steps = [
            "Check server health",
            "Check network latency",
            "Review retry settings",
        ]
    elif "null pointer" in text:
        category = "NULL_POINTER"
        evidence = "The log contains the phrase 'null pointer'."
        next_steps = [
            "Inspect the stack trace",
            "Check variable initialization",
            "Review recent changes",
        ]
    else:
        category = "UNKNOWN"
        evidence = "No configured error pattern matched."
        next_steps = [
            "Collect surrounding logs",
            "Check recent deployments",
            "Consult an approved runbook",
        ]

    return {
        "category": category,
        "evidence": evidence,
        "next_steps": next_steps,
        "approval_required_before_changes": True,
    }


if __name__ == "__main__":
    report = analyze_incident("Jenkins pipeline failed: connection timeout")
    print("Category:", report["category"])
    print("Evidence:", report["evidence"])
    print("Next steps:")
    for step in report["next_steps"]:
        print("-", step)
    print("Approval required:", report["approval_required_before_changes"])
