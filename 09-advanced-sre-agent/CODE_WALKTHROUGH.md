# Code Walkthrough — Advanced SRE Incident Correlator

This guide explains `incident_correlator.py` in plain English, then connects each step to the code.

## 1. What problem are we solving?

Imagine two read-only checks report:

- Deployment `checkout-api`: only 1 of 3 replicas is ready.
- Service `checkout-api`: no ready endpoints.

Those observations may be related. The correlator groups them and creates an investigation report. It does **not** claim that one caused the other, and it performs no infrastructure changes.

## 2. Imports and type hints

~~~python
from __future__ import annotations
from typing import Any
~~~

- `__future__.annotations` postpones evaluation of annotations. It makes type hints easier to use consistently.
- `Any` says that incoming sample fields can contain different Python object types.
- Type hints document expectations; they do not validate untrusted input at runtime.

## 3. Normalize one finding

~~~python
def normalize_finding(finding: dict[str, Any]) -> dict[str, str]:
    return {
        "namespace": str(finding.get("namespace", "default")),
        "kind": str(finding.get("kind", "Unknown")),
        "name": str(finding.get("name", "unknown")),
        "status": str(finding.get("status", "UNKNOWN")),
        "observation": str(finding.get("observation", "No observation supplied")),
    }
~~~

Line by line:

1. The function accepts a dictionary representing one observation.
2. `finding.get("namespace", "default")` reads the namespace, or uses `default` when missing.
3. `kind`, `name`, and `status` get similar fallback values so a missing field does not immediately crash this small demo.
4. `str(...)` converts values to strings so the report can display them consistently.
5. `observation` stores the human-readable evidence, such as `1/3 replicas ready`.
6. The function returns a new normalized dictionary instead of changing the input.

In a production service, validate allowed values and input size instead of relying only on defaults.

## 4. Normalize all incoming findings

~~~python
normalized = [normalize_finding(item) for item in findings]
~~~

This list comprehension calls `normalize_finding` for every item. After this line, the remaining code can rely on the same five keys for each normalized item.

## 5. Select unhealthy workloads and Services

~~~python
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
~~~

- A dictionary comprehension filters the findings.
- The key is a tuple: `(namespace, name)`. Names alone are not globally unique because two namespaces can each contain a resource called `checkout-api`.
- `workloads` keeps only unhealthy Deployment, StatefulSet, or DaemonSet findings.
- `services` keeps only unhealthy Service findings.
- Matching names are a simple demo heuristic. Real Kubernetes Services select Pods through labels; production correlation should inspect selectors, endpoints, owner references, and time windows.

## 6. Match evidence and create an incident

~~~python
for key, workload in workloads.items():
    service = services.get(key)
    if service is None:
        continue
~~~

- Iterate over each unhealthy workload.
- Look up an unhealthy Service with the same namespace/name key.
- If none exists, `continue` skips this workload rather than inventing a relationship.

When a match exists, the code constructs a report containing the title, severity label, hypothesis, evidence, and next checks. The word **hypothesis** is deliberate: matching symptoms are not proof of root cause.

## 7. Make safety explicit

~~~python
"decision": "INVESTIGATE_ONLY",
"changes_performed": False,
~~~

These fields tell a reader that the sample is for investigation only. They are not a substitute for security controls, and this file has no code that can mutate a cluster. If remediation is added later, approval must be enforced by a separate, validated code path—not merely by a string in a report.

## 8. Main function and sample data

The `main()` function creates two synthetic findings, calls `correlate(sample_findings)`, and prints the returned incident. Synthetic data makes the example safe to run on a laptop without kubeconfig, cluster access, API credentials, or third-party dependencies.

The final condition:

~~~python
if __name__ == "__main__":
    main()
~~~

means Python runs `main()` only when this file is executed directly. Importing it from a unit test does not automatically print the demo output.

## 9. Run and test

From the repository root:

~~~bash
python 09-advanced-sre-agent/incident_correlator.py
python -m unittest discover -s 09-advanced-sre-agent -v
~~~

The tests check that matching unhealthy resources are correlated, resources in different namespaces are not matched, a healthy Service is not treated as a failure, and defaults are supplied for missing fields.

## 10. Limitations worth saying in an interview

- Same-name matching is only a teaching heuristic; Kubernetes Service selectors and endpoint membership are the real relationship to inspect.
- The sample has no timestamps, so it cannot establish whether symptoms occurred in the same incident window.
- It does not query metrics, events, logs, a vector database, an LLM, or a live cluster.
- Severity is illustrative, not a calibrated incident priority.
- The output is a lead for investigation, not an automated root-cause determination.

A strong next version should add selector/owner-reference correlation, event timelines, source citations, redaction, runbook retrieval, and integration tests against a disposable Kubernetes cluster.
