"""Example 2: triage multiple sanitized log lines into a safe incident summary.

This script only analyzes provided sample strings. It never runs remediation.
"""


def classify_line(line: str) -> str:
    text = line.lower()
    if "timeout" in text:
        return "TIMEOUT"
    if "disk full" in text or "no space left" in text:
        return "DISK_FULL"
    if "permission denied" in text:
        return "PERMISSION_DENIED"
    return "UNKNOWN"


RECOMMENDATIONS = {
    "TIMEOUT": "Check network path, DNS, and upstream health.",
    "DISK_FULL": "Use approved read-only checks to inspect filesystem usage.",
    "PERMISSION_DENIED": "Verify the service identity and least-privilege permissions.",
    "UNKNOWN": "Collect surrounding logs and consult an approved runbook.",
}


def triage(log_lines: list[str]) -> dict:
    findings = []
    for line in log_lines:
        category = classify_line(line)
        findings.append({
            "category": category,
            "evidence": line,
            "recommendation": RECOMMENDATIONS[category],
        })
    return {
        "incident_count": len(findings),
        "findings": findings,
        "approval_required_before_changes": True,
        "execution_performed": False,
    }


if __name__ == "__main__":
    sample_logs = [
        "Jenkins stage failed: connection timeout",
        "Runner error: no space left on device",
        "Deploy step failed: permission denied",
    ]
    result = triage(sample_logs)
    print("Incident count:", result["incident_count"])
    for finding in result["findings"]:
        print(f"- {finding['category']}: {finding['recommendation']}")
    print("Approval required:", result["approval_required_before_changes"])
    print("Execution performed:", result["execution_performed"])
