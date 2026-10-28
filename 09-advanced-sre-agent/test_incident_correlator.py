"""Unit tests for the offline incident correlation prototype."""
import unittest

from incident_correlator import correlate, normalize_finding


class IncidentCorrelatorTests(unittest.TestCase):
    def test_correlates_matching_unhealthy_workload_and_service(self):
        findings = [
            {"namespace": "production", "kind": "Deployment", "name": "checkout-api",
             "status": "ISSUE", "observation": "1/3 replicas ready"},
            {"namespace": "production", "kind": "Service", "name": "checkout-api",
             "status": "ISSUE", "observation": "no ready endpoints"},
        ]
        incidents = correlate(findings)
        self.assertEqual(len(incidents), 1)
        self.assertEqual(incidents[0]["decision"], "INVESTIGATE_ONLY")
        self.assertFalse(incidents[0]["changes_performed"])
        self.assertEqual(len(incidents[0]["evidence"]), 2)

    def test_does_not_correlate_different_namespaces(self):
        findings = [
            {"namespace": "production", "kind": "Deployment", "name": "checkout-api",
             "status": "ISSUE", "observation": "1/3 replicas ready"},
            {"namespace": "staging", "kind": "Service", "name": "checkout-api",
             "status": "ISSUE", "observation": "no ready endpoints"},
        ]
        self.assertEqual(correlate(findings), [])

    def test_does_not_correlate_healthy_service(self):
        findings = [
            {"namespace": "production", "kind": "Deployment", "name": "checkout-api",
             "status": "ISSUE", "observation": "1/3 replicas ready"},
            {"namespace": "production", "kind": "Service", "name": "checkout-api",
             "status": "OK", "observation": "3 ready endpoints"},
        ]
        self.assertEqual(correlate(findings), [])

    def test_normalize_supplies_safe_defaults(self):
        result = normalize_finding({})
        self.assertEqual(result["namespace"], "default")
        self.assertEqual(result["kind"], "Unknown")
        self.assertEqual(result["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
