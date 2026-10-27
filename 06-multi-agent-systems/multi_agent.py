"""A deterministic simulation of specialist roles and a handoff."""


def investigator_agent(logs: str) -> dict:
    text = logs.lower()
    if "timeout" in text:
        return {"finding": "Likely network or server timeout", "evidence": "timeout"}
    if "null pointer" in text:
        return {"finding": "Likely null value or initialization issue", "evidence": "null pointer"}
    return {"finding": "Cause not identified", "evidence": "No known pattern matched"}


def runbook_agent(finding: dict) -> str:
    if finding["evidence"] == "timeout":
        return "Check network path and server health."
    if finding["evidence"] == "null pointer":
        return "Check variable initialization and recent changes."
    return "Gather more evidence and consult approved runbooks."


def reviewer_agent(finding: dict, recommendation: str) -> dict:
    supported = finding["evidence"] != "No known pattern matched"
    return {
        "finding": finding["finding"],
        "recommendation": recommendation,
        "supported_by_known_pattern": supported,
        "status": "Approval required before any remediation.",
    }


if __name__ == "__main__":
    finding = investigator_agent("Jenkins connection timeout")
    recommendation = runbook_agent(finding)
    review = reviewer_agent(finding, recommendation)
    print("Investigation:", review["finding"] + ".")
    print("Recommendation:", review["recommendation"])
    print("Status:", review["status"])
