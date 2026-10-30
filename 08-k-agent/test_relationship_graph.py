"""Tests for Kubernetes Service, Pod selector, ownership, and Endpoints relationships."""
import unittest

from relationship_graph import (
    build_relationship_report,
    endpoint_summary,
    selector_matches,
    service_pod_relationship,
)


def pod(name, labels, ready=True, namespace="payments", owners=None):
    return {
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": labels,
            "ownerReferences": owners or [],
        },
        "status": {
            "conditions": [{"type": "Ready", "status": "True" if ready else "False"}]
        },
    }


class RelationshipGraphTests(unittest.TestCase):
    def test_selector_requires_every_key_to_match(self):
        self.assertTrue(selector_matches({"app": "api", "tier": "backend"}, {"app": "api", "tier": "backend"}))
        self.assertFalse(selector_matches({"app": "api", "tier": "backend"}, {"app": "api"}))

    def test_service_matches_only_same_namespace_and_selector(self):
        service = {
            "metadata": {"name": "checkout", "namespace": "payments"},
            "spec": {"selector": {"app": "checkout", "tier": "api"}},
        }
        pods = [
            pod("checkout-a", {"app": "checkout", "tier": "api"}, True),
            pod("checkout-b", {"app": "checkout", "tier": "api"}, False),
            pod("other", {"app": "other", "tier": "api"}, True),
            pod("wrong-namespace", {"app": "checkout", "tier": "api"}, True, "default"),
        ]
        result = service_pod_relationship(service, pods)
        self.assertEqual(result["matched_pods"], ["checkout-a", "checkout-b"])
        self.assertEqual(result["ready_pods"], ["checkout-a"])
        self.assertEqual(result["diagnosis"], "MATCHED_PODS_NOT_READY")

    def test_empty_selector_is_not_treated_as_match_all(self):
        service = {"metadata": {"name": "external", "namespace": "payments"}, "spec": {"selector": {}}}
        self.assertEqual(service_pod_relationship(service, [pod("any", {"app": "x"})])["diagnosis"], "NO_SELECTOR")

    def test_endpoints_counts_ready_and_not_ready_addresses(self):
        endpoints = {
            "metadata": {"name": "checkout", "namespace": "payments"},
            "subsets": [{
                "addresses": [{"ip": "10.0.0.1", "targetRef": {"name": "checkout-a"}}],
                "notReadyAddresses": [{"ip": "10.0.0.2", "targetRef": {"name": "checkout-b"}}],
            }],
        }
        result = endpoint_summary(endpoints)
        self.assertEqual(result["ready_count"], 1)
        self.assertEqual(result["not_ready_count"], 1)
        self.assertEqual(result["ready_addresses"], ["checkout-a"])

    def test_report_includes_one_hop_owner_references(self):
        service = {
            "metadata": {"name": "checkout", "namespace": "payments"},
            "spec": {"selector": {"app": "checkout"}},
        }
        owned_pod = pod("checkout-a", {"app": "checkout"}, owners=[
            {"kind": "ReplicaSet", "name": "checkout-abc", "uid": "rs-1", "controller": True}
        ])
        report = build_relationship_report(service, [owned_pod])
        self.assertEqual(report["pod_ownership"][0]["owner_references"][0]["kind"], "ReplicaSet")
        self.assertEqual(report["pod_ownership"][0]["owner_references"][0]["name"], "checkout-abc")


if __name__ == "__main__":
    unittest.main()
