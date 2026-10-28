"""Offline incident correlation prototype.

Consumes normalized findings only. It does not connect to Kubernetes, call an
LLM, run shell commands, or change infrastructure.
"""
from __future__ import annotations

from typing import Any


def normalize_finding(finding: dict[str, Any]) -> dict[str, str]:
    """Extract stable identity and status fields from one normalized finding."""
    return {
        "namespace": str(finding.get("namespace", "default")),
        "kind": str(finding.get("kind", "Unknown")),
        "name": str(finding.get("name", "unknown")),
        "status": str(finding.get("status", "UNKNOWN")),
        "observation": str(finding.get("observation", "No observation supplied")),
    }


def correlate(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create cautious hypotheses from matching workload and Service names."""
    normalized = [normalize_finding(item) for item in findings]
    incidents: list[dict[str, Any]] = []
    workloads = {
        (item["namespace"], item["name"]): item
        for item in normalized
        if item["kind"] in {"Deployment", "StatefulSet", "DaemonSet"}
        and item["status"] == "ISSUE"
    }
    services = {
        (item["namespace"], item["name"]): item
        for item in normalized
        if item["kind"] == "Service" and item["status"] == "ISSUE"
    }

    for key, workload in workloads.items():
        service = services.get(key)
        if service is None:
            continue
        namespace, name = key
        incidents.append({
            "title": f"Incident: {name} in namespace {namespace}",
            "severity": "HIGH",
            "hypothesis": (
                "Workload readiness and Service endpoint symptoms may be related; "
                "this correlation does not prove root cause."
            ),
            "evidence": [
                f'{workload["kind"]}/{name}: {workload["observation"]}',
                f'Service/{name}: {service["observation"]}',
            ],
            "next_checks": [
                "Inspect Pods owned by the workload and their Warning events.",
                "Check readiness probes, selector labels, and recent rollout history.",
                "Compare application errors and latency in the same time window.",
            ],
            "decision": "INVESTIGATE_ONLY",
            "changes_performed": False,
        })
    return incidents


def main() -> None:
    """Run the example against synthetic normalized findings."""
    sample_findings = [
        {"namespace": "production", "kind": "Deployment", "name": "checkout-api",
         "status": "ISSUE", "observation": "1/3 replicas ready"},
        {"namespace": "production", "kind": "Service", "name": "checkout-api",
         "status": "ISSUE", "observation": "no ready endpoints"},
    ]
    incidents = correlate(sample_findings)
    if not incidents:
        print("No correlated incidents found in the supplied sample.")
        return
    for incident in incidents:
        print(incident["title"])
        print(f'Severity: {incident["severity"]}')
        print(f'Hypothesis: {incident["hypothesis"]}')
        print("Evidence:")
        for evidence in incident["evidence"]:
            print(f"  - {evidence}")
        print("Next checks:")
        for check in incident["next_checks"]:
            print(f"  - {check}")
        print(f'Decision: {incident["decision"]} (no infrastructure changes performed)')


if __name__ == "__main__":
    main()
