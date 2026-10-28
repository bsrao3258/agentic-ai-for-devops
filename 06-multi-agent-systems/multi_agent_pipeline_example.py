"""Example 2: deterministic specialist-agent pipeline with disagreement handling.

Functions simulate roles; they are not independent LLM-powered agents.
"""


def log_investigator(log_text: str) -> dict:
    text = log_text.lower()
    if "timeout" in text:
        return {"category": "TIMEOUT", "evidence": "connection timeout"}
    if "disk full" in text:
        return {"category": "DISK_FULL", "evidence": "disk full"}
    return {"category": "UNKNOWN", "evidence": "no recognized phrase"}


def runbook_researcher(category: str) -> str:
    return {
        "TIMEOUT": "Check DNS resolution, network path, and upstream health.",
        "DISK_FULL": "Inspect filesystem usage and identify large files safely.",
        "UNKNOWN": "Search approved runbooks after collecting more evidence.",
    }[category]


def reviewer(investigation: dict, recommendation: str) -> dict:
    supported = investigation["category"] != "UNKNOWN"
    return {
        "category": investigation["category"],
        "evidence": investigation["evidence"],
        "recommendation": recommendation,
        "confidence_note": "Known pattern matched" if supported else "Insufficient evidence",
        "approval_required": True,
    }


def run_pipeline(log_text: str) -> dict:
    finding = log_investigator(log_text)
    recommendation = runbook_researcher(finding["category"])
    return reviewer(finding, recommendation)


if __name__ == "__main__":
    for sample in ("API connection timeout", "Node disk full", "Unexpected exit code"):
        print(run_pipeline(sample))
