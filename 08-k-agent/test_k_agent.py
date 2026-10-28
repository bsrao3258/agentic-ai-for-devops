"""Unit tests for pure K-Agent logic; no Kubernetes cluster is required.

Run from repository root:
    python -m unittest discover -s 08-k-agent -v
"""
import unittest

from k_agent import classify_node, classify_pod, classify_workload, known_recommendation


class KAgentClassificationTests(unittest.TestCase):
    def test_running_pod_without_restarts_is_ok(self):
        pod = {
            "metadata": {"name": "api-123", "namespace": "default"},
            "status": {"phase": "Running", "containerStatuses": [{"restartCount": 0, "state": {"running": {}}}]},
        }
        finding = classify_pod(pod)
        self.assertEqual(finding["health"], "OK")
        self.assertEqual(finding["restart_count"], 0)

    def test_crashloop_pod_is_issue_and_has_known_next_step(self):
        pod = {
            "metadata": {"name": "api-123", "namespace": "default"},
            "status": {
                "phase": "Running",
                "containerStatuses": [
                    {"restartCount": 5, "state": {"waiting": {"reason": "CrashLoopBackOff"}}}
                ],
            },
        }
        finding = classify_pod(pod)
        self.assertEqual(finding["health"], "ISSUE")
        self.assertEqual(known_recommendation(finding)["action"], "restart_workload")

    def test_image_pull_error_does_not_recommend_restart(self):
        finding = {"kind": "Pod", "health": "ISSUE", "reason": "ImagePullBackOff"}
        self.assertEqual(known_recommendation(finding)["action"], "investigate_only")

    def test_unknown_error_requests_analysis(self):
        finding = {"kind": "Pod", "health": "ISSUE", "reason": "MysteryFailure"}
        recommendation = known_recommendation(finding)
        self.assertEqual(recommendation["action"], "investigate_only")
        self.assertIn("Analysis is required", recommendation["why"])

    def test_deployment_not_ready(self):
        deployment = {
            "metadata": {"name": "web", "namespace": "staging"},
            "spec": {"replicas": 3},
            "status": {"readyReplicas": 1, "conditions": []},
        }
        finding = classify_workload("Deployment", deployment)
        self.assertEqual(finding["health"], "ISSUE")
        self.assertEqual(finding["ready"], 1)
        self.assertEqual(finding["desired"], 3)

    def test_daemonset_uses_scheduled_and_ready_counts(self):
        daemonset = {
            "metadata": {"name": "node-agent", "namespace": "kube-system"},
            "status": {"desiredNumberScheduled": 5, "numberReady": 4, "conditions": []},
        }
        finding = classify_workload("DaemonSet", daemonset)
        self.assertEqual(finding["health"], "ISSUE")
        self.assertEqual(finding["reason"], "4/5 replicas ready")

    def test_ready_node(self):
        node = {
            "metadata": {"name": "worker-1"},
            "status": {"conditions": [{"type": "Ready", "status": "True"}]},
        }
        self.assertEqual(classify_node(node)["health"], "OK")

    def test_not_ready_node(self):
        node = {
            "metadata": {"name": "worker-2"},
            "status": {"conditions": [{"type": "Ready", "status": "False", "reason": "KubeletNotReady"}]},
        }
        finding = classify_node(node)
        self.assertEqual(finding["health"], "ISSUE")
        self.assertEqual(finding["reason"], "KubeletNotReady")


if __name__ == "__main__":
    unittest.main()
