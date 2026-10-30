"""Run a synthetic Service-to-Pod relationship investigation.

No cluster credentials or third-party packages are needed. This example is
intentionally offline and prints evidence, not an asserted root cause.
"""
from __future__ import annotations

from relationship_graph import build_relationship_report


service = {
    "metadata": {"name": "checkout-api", "namespace": "production"},
    "spec": {"selector": {"app": "checkout", "component": "api"}},
}
pods = [
    {
        "metadata": {
            "name": "checkout-api-7d9f-a1",
            "namespace": "production",
            "labels": {"app": "checkout", "component": "api"},
            "ownerReferences": [
                {"kind": "ReplicaSet", "name": "checkout-api-7d9f", "uid": "rs-123", "controller": True}
            ],
        },
        "status": {"conditions": [{"type": "Ready", "status": "True"}]},
    },
    {
        "metadata": {
            "name": "checkout-api-7d9f-a2",
            "namespace": "production",
            "labels": {"app": "checkout", "component": "api"},
            "ownerReferences": [
                {"kind": "ReplicaSet", "name": "checkout-api-7d9f", "uid": "rs-123", "controller": True}
            ],
        },
        "status": {"conditions": [{"type": "Ready", "status": "False"}]},
    },
    {
        "metadata": {
            "name": "metrics-agent",
            "namespace": "production",
            "labels": {"app": "metrics", "component": "agent"},
        },
        "status": {"conditions": [{"type": "Ready", "status": "True"}]},
    },
]
endpoints = {
    "metadata": {"name": "checkout-api", "namespace": "production"},
    "subsets": [{
        "addresses": [{"ip": "10.10.0.11", "targetRef": {"name": "checkout-api-7d9f-a1"}}],
        "notReadyAddresses": [{"ip": "10.10.0.12", "targetRef": {"name": "checkout-api-7d9f-a2"}}],
    }],
}


def main() -> None:
    report = build_relationship_report(service, pods, endpoints)
    relation = report["service_relationship"]
    endpoint_data = report["endpoint_summary"]

    print(f"Service: {relation['service']} ({relation['namespace']})")
    print(f"Selector: {relation['selector']}")
    print(f"Matched Pods: {relation['matched_pod_count']}")
    print(f"Ready matched Pods: {relation['ready_pod_count']}")
    print(f"Evidence classification: {relation['diagnosis']}")
    print(f"Endpoint addresses: {endpoint_data['ready_count']} ready, "
          f"{endpoint_data['not_ready_count']} not ready")
    print("Pod ownership:")
    for item in report["pod_ownership"]:
        owners = item["owner_references"] or [{"kind": "Unknown", "name": "no owner reference"}]
        for owner in owners:
            print(f"  {item['pod']} -> {owner['kind']}/{owner['name']}")
    print("Conclusion: investigate readiness and endpoint membership; no change was made.")


if __name__ == "__main__":
    main()
