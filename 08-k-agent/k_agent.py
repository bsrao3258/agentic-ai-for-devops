"""K-Agent: conservative Kubernetes status and troubleshooting assistant.

Default behavior is read-only. The optional restart action only patches the pod
template of a Deployment, StatefulSet, or DaemonSet after exact interactive
approval. It never deletes Pods or modifies Services, CRDs, Nodes, PVCs, or RBAC.

Install: python -m pip install -r 08-k-agent/requirements.txt
Run:     python 08-k-agent/k_agent.py --namespace default
Watch:   python 08-k-agent/k_agent.py --all-namespaces --watch --interval 30
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any

try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
except ImportError:
    client = None
    config = None

    class ApiException(Exception):
        status = None
        reason = "Kubernetes client library is not installed"


RESTARTABLE_KINDS = {"Deployment", "StatefulSet", "DaemonSet"}
KNOWN_RESTART_REASONS = {
    "CrashLoopBackOff",
    "ProgressDeadlineExceeded",
    "ReplicaFailure",
    "FailedCreate",
    "Error",
}
UNKNOWN_MESSAGE = "Analysis is required: the agent has no safe, evidence-backed known solution."


def _get(obj: Any, *path: str, default: Any = None) -> Any:
    """Safely read nested dictionary keys or Kubernetes model attributes."""
    value = obj
    for part in path:
        if value is None:
            return default
        if isinstance(value, dict):
            # Kubernetes API dictionaries use camelCase while client models use snake_case.
            camel = part.split("_")[0] + "".join(piece.title() for piece in part.split("_")[1:])
            value = value.get(part, value.get(camel))
        else:
            value = getattr(value, part, None)
    return default if value is None else value


def _redact(text: str) -> str:
    """Mask common secret patterns before logs are printed or serialized."""
    patterns = [
        (r"(?i)(authorization\s*[:=]\s*bearer\s+)\S+", r"\1[REDACTED]"),
        (r"(?i)((?:password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token)\s*[:=]\s*)[^\s,;]+", r"\1[REDACTED]"),
        (r"(?i)(AKIA[0-9A-Z]{16})", "[REDACTED_AWS_ACCESS_KEY]"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text


def _name(obj: Any) -> str:
    return str(_get(obj, "metadata", "name", default="unknown"))


def _namespace(obj: Any) -> str:
    return str(_get(obj, "metadata", "namespace", default="default"))


def classify_pod(pod: Any) -> dict[str, Any]:
    """Return a concise status finding for a Pod object or Kubernetes-style dict."""
    phase = _get(pod, "status", "phase", default="Unknown")
    statuses = _get(pod, "status", "container_statuses", default=None)
    if statuses is None:
        statuses = _get(pod, "status", "containerStatuses", default=[]) or []
    reasons: list[str] = []
    restart_count = 0
    for status in statuses or []:
        reason = _get(status, "state", "waiting", "reason")
        if reason:
            reasons.append(str(reason))
        terminated_reason = _get(status, "state", "terminated", "reason")
        if terminated_reason:
            reasons.append(str(terminated_reason))
        restart_count += int(_get(status, "restart_count", default=_get(status, "restartCount", default=0)) or 0)

    if phase == "Succeeded":
        health = "OK"
    elif phase == "Running" and not reasons and restart_count < 4:
        health = "OK"
    else:
        health = "ISSUE"

    reason = reasons[0] if reasons else str(phase)
    return {
        "kind": "Pod",
        "namespace": _namespace(pod),
        "name": _name(pod),
        "health": health,
        "reason": reason,
        "restart_count": restart_count,
        "message": f"Pod phase={phase}; restart_count={restart_count}; reasons={reasons or ['none reported']}",
    }


def classify_workload(kind: str, obj: Any) -> dict[str, Any]:
    """Check replica readiness for Deployments, StatefulSets, and DaemonSets."""
    desired = int(_get(obj, "spec", "replicas", default=1) or 0)
    if kind == "DaemonSet":
        desired = int(_get(obj, "status", "desired_number_scheduled", default=0) or 0)
        ready = int(_get(obj, "status", "number_ready", default=0) or 0)
    else:
        ready = int(_get(obj, "status", "ready_replicas", default=0) or 0)
    conditions = _get(obj, "status", "conditions", default=[]) or []
    bad_conditions = []
    for condition in conditions:
        condition_type = _get(condition, "type", default="")
        condition_status = str(_get(condition, "status", default=""))
        reason = _get(condition, "reason", default=condition_type)
        if condition_type == "ReplicaFailure" and condition_status == "True":
            bad_conditions.append(str(reason))
        elif condition_type == "Progressing" and reason == "ProgressDeadlineExceeded":
            bad_conditions.append(str(reason))
    healthy = desired == ready and not bad_conditions
    reason = "Ready" if healthy else (bad_conditions[0] if bad_conditions else f"{ready}/{desired} replicas ready")
    return {
        "kind": kind,
        "namespace": _namespace(obj),
        "name": _name(obj),
        "health": "OK" if healthy else "ISSUE",
        "reason": reason,
        "ready": ready,
        "desired": desired,
        "message": f"{kind} has {ready}/{desired} ready replicas; conditions={bad_conditions or ['no blocking condition reported']}",
    }


def classify_node(node: Any) -> dict[str, Any]:
    conditions = _get(node, "status", "conditions", default=[]) or []
    ready = next((c for c in conditions if _get(c, "type") == "Ready"), None)
    is_ready = ready is not None and str(_get(ready, "status", default="False")) == "True"
    reason = "Ready" if is_ready else str(_get(ready, "reason", default="NodeNotReady"))
    return {
        "kind": "Node", "namespace": "cluster", "name": _name(node),
        "health": "OK" if is_ready else "ISSUE", "reason": reason,
        "message": str(_get(ready, "message", default="Node Ready condition is missing or not True")),
    }


def classify_pvc(pvc: Any) -> dict[str, Any]:
    phase = _get(pvc, "status", "phase", default="Unknown")
    healthy = phase == "Bound"
    return {
        "kind": "PersistentVolumeClaim", "namespace": _namespace(pvc), "name": _name(pvc),
        "health": "OK" if healthy else "ISSUE", "reason": str(phase),
        "message": f"PVC phase is {phase}; inspect storage class, capacity, and provisioner events if not Bound.",
    }


def classify_job(job: Any) -> dict[str, Any]:
    conditions = _get(job, "status", "conditions", default=[]) or []
    failed = any(_get(c, "type") == "Failed" and str(_get(c, "status")) == "True" for c in conditions)
    succeeded = int(_get(job, "status", "succeeded", default=0) or 0)
    failed_count = int(_get(job, "status", "failed", default=0) or 0)
    healthy = succeeded > 0 and not failed
    reason = "Failed" if failed else ("Complete" if healthy else "Running or Pending")
    return {
        "kind": "Job", "namespace": _namespace(job), "name": _name(job),
        "health": "OK" if healthy else "ISSUE", "reason": reason,
        "message": f"Job succeeded={succeeded}; failed={failed_count}.",
    }


def known_recommendation(finding: dict[str, Any]) -> dict[str, str]:
    """Recommend safe next steps; never claim a recommendation guarantees recovery."""
    kind = finding.get("kind", "")
    reason = str(finding.get("reason", ""))
    reason_lower = reason.lower()
    if kind == "Pod":
        if "imagepullbackoff" in reason_lower or "errimagepull" in reason_lower:
            return {"action": "investigate_only", "why": "The image could not be pulled; verify image name/tag, registry reachability, and imagePullSecrets. A restart alone does not fix bad image credentials or a missing image."}
        if "oomkilled" in reason_lower:
            return {"action": "investigate_only", "why": "The container was killed for memory pressure; inspect memory limits, usage, and previous logs before changing resources."}
        if "crashloopbackoff" in reason_lower or reason_lower == "error":
            return {"action": "restart_workload", "why": "The container is repeatedly failing. A controller rollout restart is a possible attempt for transient state, but may not fix a bad image, configuration, or application bug. Review previous logs and events first."}
        if "pending" in reason_lower:
            return {"action": "investigate_only", "why": "The Pod is not scheduled or not ready; inspect scheduler events, resource requests, node capacity, affinity, taints, and PVC binding. Restarting is not a suitable first fix."}
    if kind in RESTARTABLE_KINDS and reason in KNOWN_RESTART_REASONS:
        return {"action": "restart_workload", "why": f"{reason} was reported for this controller. A rollout restart may help only if the failure is transient; review related Pod logs and warning events first. This does not guarantee recovery."}
    if kind in RESTARTABLE_KINDS and finding.get("health") == "ISSUE":
        return {"action": "investigate_only", "why": "Replica readiness is below the desired count, but the cause is not specific enough for a safe automatic remedy. Inspect Pods, events, logs, image, resources, and scheduling."}
    return {"action": "investigate_only", "why": UNKNOWN_MESSAGE}


class KAgent:
    """Read-only Kubernetes inventory and diagnostics with optional approved restarts."""

    def __init__(self, namespace: str | None = None):
        if client is None or config is None:
            raise RuntimeError("Kubernetes SDK missing. Install 08-k-agent/requirements.txt")
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        self.namespace = namespace
        self.core = client.CoreV1Api()
        self.apps = client.AppsV1Api()
        self.batch = client.BatchV1Api()
        self.networking = client.NetworkingV1Api()
        self.storage = client.StorageV1Api()
        self.autoscaling = client.AutoscalingV2Api()
        self.policy = client.PolicyV1Api()
        self.rbac = client.RbacAuthorizationV1Api()
        self.apiextensions = client.ApiextensionsV1Api()

    def _list(self, method: Any, namespaced: bool = False) -> list[Any]:
        """Call a Kubernetes list API; report failures instead of treating them as healthy."""
        try:
            if self.namespace and namespaced:
                return method(namespace=self.namespace).items
            return method().items
        except Exception as exc:
            status = getattr(exc, "status", "?")
            reason = getattr(exc, "reason", str(exc))
            print(f"[WARN] API read failed ({status}): {reason}", file=sys.stderr)
            return []

    def inspect(self, include_logs: bool = True) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []
        inventory: dict[str, int] = {}

        pod_method = self.core.list_namespaced_pod if self.namespace else self.core.list_pod_for_all_namespaces
        pods = self._list(pod_method, namespaced=bool(self.namespace))
        inventory["Pods"] = len(pods)
        for pod in pods:
            finding = classify_pod(pod)
            findings.append(finding)
            if include_logs and finding["health"] == "ISSUE":
                finding["log_excerpt"] = self._pod_logs(pod)

        core_resources = [
            ("Services", self.core.list_namespaced_service if self.namespace else self.core.list_service_for_all_namespaces, True),
            ("Endpoints", self.core.list_namespaced_endpoints if self.namespace else self.core.list_endpoints_for_all_namespaces, True),
            ("ConfigMaps", self.core.list_namespaced_config_map if self.namespace else self.core.list_config_map_for_all_namespaces, True),
            ("ServiceAccounts", self.core.list_namespaced_service_account if self.namespace else self.core.list_service_account_for_all_namespaces, True),
            ("SecretsMetadataOnly", self.core.list_namespaced_secret if self.namespace else self.core.list_secret_for_all_namespaces, True),
            ("ResourceQuotas", self.core.list_namespaced_resource_quota if self.namespace else self.core.list_resource_quota_for_all_namespaces, True),
            ("LimitRanges", self.core.list_namespaced_limit_range if self.namespace else self.core.list_limit_range_for_all_namespaces, True),
            ("PVCs", self.core.list_namespaced_persistent_volume_claim if self.namespace else self.core.list_persistent_volume_claim_for_all_namespaces, True),
        ]
        endpoints: list[Any] = []
        services: list[Any] = []
        for label, method, namespaced in core_resources:
            objects = self._list(method, namespaced=namespaced)
            inventory[label] = len(objects)
            if label == "Endpoints":
                endpoints = objects
            elif label == "Services":
                services = objects
            elif label == "PVCs":
                findings.extend(classify_pvc(obj) for obj in objects)

        endpoint_map = {(_namespace(ep), _name(ep)): ep for ep in endpoints}
        for svc in services:
            selector = _get(svc, "spec", "selector", default={}) or {}
            if not selector:
                continue
            ep = endpoint_map.get((_namespace(svc), _name(svc)))
            subsets = _get(ep, "subsets", default=[]) or []
            ready_addresses = sum(len(_get(subset, "addresses", default=[]) or []) for subset in subsets)
            if ready_addresses == 0:
                findings.append({
                    "kind": "Service", "namespace": _namespace(svc), "name": _name(svc),
                    "health": "ISSUE", "reason": "NoReadyEndpoints",
                    "message": "Service has a selector but no ready endpoint addresses. Check selector labels, Pod readiness, and targetPort.",
                })

        nodes = self._list(self.core.list_node)
        inventory["Nodes"] = len(nodes)
        findings.extend(classify_node(node) for node in nodes)

        namespaces = self._list(self.core.list_namespace)
        inventory["Namespaces"] = len(namespaces)
        for ns in namespaces:
            phase = _get(ns, "status", "phase", default="Unknown")
            if phase != "Active":
                findings.append({"kind": "Namespace", "namespace": _name(ns), "name": _name(ns), "health": "ISSUE", "reason": str(phase), "message": f"Namespace phase is {phase}."})

        workload_specs = [
            ("Deployment", self.apps.list_namespaced_deployment if self.namespace else self.apps.list_deployment_for_all_namespaces, True),
            ("StatefulSet", self.apps.list_namespaced_stateful_set if self.namespace else self.apps.list_stateful_set_for_all_namespaces, True),
            ("DaemonSet", self.apps.list_namespaced_daemon_set if self.namespace else self.apps.list_daemon_set_for_all_namespaces, True),
            ("ReplicaSet", self.apps.list_namespaced_replica_set if self.namespace else self.apps.list_replica_set_for_all_namespaces, True),
            ("Job", self.batch.list_namespaced_job if self.namespace else self.batch.list_job_for_all_namespaces, True),
            ("CronJob", self.batch.list_namespaced_cron_job if self.namespace else self.batch.list_cron_job_for_all_namespaces, True),
            ("Ingress", self.networking.list_namespaced_ingress if self.namespace else self.networking.list_ingress_for_all_namespaces, True),
            ("NetworkPolicy", self.networking.list_namespaced_network_policy if self.namespace else self.networking.list_network_policy_for_all_namespaces, True),
            ("HPA", self.autoscaling.list_namespaced_horizontal_pod_autoscaler if self.namespace else self.autoscaling.list_horizontal_pod_autoscaler_for_all_namespaces, True),
            ("PDB", self.policy.list_namespaced_pod_disruption_budget if self.namespace else self.policy.list_pod_disruption_budget_for_all_namespaces, True),
            ("Roles", self.rbac.list_namespaced_role if self.namespace else self.rbac.list_role_for_all_namespaces, True),
            ("RoleBindings", self.rbac.list_namespaced_role_binding if self.namespace else self.rbac.list_role_binding_for_all_namespaces, True),
        ]
        for kind, method, namespaced in workload_specs:
            objects = self._list(method, namespaced=namespaced)
            inventory[kind] = len(objects)
            if kind in {"Deployment", "StatefulSet", "DaemonSet"}:
                findings.extend(classify_workload(kind, obj) for obj in objects)
            elif kind == "Job":
                findings.extend(classify_job(obj) for obj in objects)
            elif kind == "CronJob":
                for obj in objects:
                    if bool(_get(obj, "spec", "suspend", default=False)):
                        findings.append({"kind": kind, "namespace": _namespace(obj), "name": _name(obj), "health": "INFO", "reason": "Suspended", "message": "CronJob is suspended by configuration; verify this is intentional."})

        cluster_resources = [
            ("PersistentVolumes", self.core.list_persistent_volume),
            ("StorageClasses", self.storage.list_storage_class),
            ("CSIDrivers", self.storage.list_csi_driver),
            ("ClusterRoles", self.rbac.list_cluster_role),
            ("ClusterRoleBindings", self.rbac.list_cluster_role_binding),
            ("CustomResourceDefinitions", self.apiextensions.list_custom_resource_definition),
        ]
        for label, method in cluster_resources:
            objects = self._list(method)
            inventory[label] = len(objects)
            if label == "CustomResourceDefinitions":
                for crd in objects:
                    conditions = _get(crd, "status", "conditions", default=[]) or []
                    established = any(_get(c, "type") == "Established" and str(_get(c, "status")) == "True" for c in conditions)
                    if not established:
                        findings.append({"kind": "CustomResourceDefinition", "namespace": "cluster", "name": _name(crd), "health": "ISSUE", "reason": "NotEstablished", "message": "CRD is not reporting Established=True; inspect CRD conditions and API server events."})

        event_method = self.core.list_namespaced_event if self.namespace else self.core.list_event_for_all_namespaces
        events = self._list(event_method, namespaced=bool(self.namespace))
        warning_events = []
        for event in events:
            if str(_get(event, "type", default="")) == "Warning":
                warning_events.append({
                    "namespace": _namespace(event),
                    "reason": str(_get(event, "reason", default="Unknown")),
                    "object": str(_get(event, "involved_object", "name", default=_get(event, "regarding", "name", default="unknown"))),
                    "message": _redact(str(_get(event, "message", default=""))[:800]),
                    "count": int(_get(event, "count", default=1) or 1),
                })
        inventory["WarningEvents"] = len(warning_events)

        restart_candidates = []
        for finding in findings:
            if finding.get("health") != "ISSUE":
                continue
            recommendation = known_recommendation(finding)
            finding["recommendation"] = recommendation["why"]
            finding["suggested_action"] = recommendation["action"]
            if recommendation["action"] == "restart_workload" and finding.get("kind") in RESTARTABLE_KINDS:
                restart_candidates.append(finding)

        return {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "scope": self.namespace or "all namespaces",
            "inventory": inventory,
            "findings": findings,
            "warning_events": warning_events[-100:],
            "restart_candidates": restart_candidates,
            "limitations": [
                "Resources are checked only when this identity has permission; WARN messages mean the report may be incomplete.",
                "CRD definitions are inventoried, but arbitrary custom-resource instances are not automatically interpreted.",
                "This is a snapshot or polling loop, not an event-driven controller.",
                "A rollout restart is not a universal fix and can disrupt workloads; review evidence and approve each exact controller separately.",
            ],
        }

    def _pod_logs(self, pod: Any) -> list[dict[str, str]]:
        """Read bounded logs from failing containers without reading environment secrets."""
        name, namespace = _name(pod), _namespace(pod)
        statuses = _get(pod, "status", "container_statuses", default=None)
        if statuses is None:
            statuses = _get(pod, "status", "containerStatuses", default=[]) or []
        result = []
        for status in statuses or []:
            container_name = _get(status, "name", default="")
            waiting_reason = _get(status, "state", "waiting", "reason", default="")
            terminated_reason = _get(status, "last_state", "terminated", "reason", default=_get(status, "lastState", "terminated", "reason", default=""))
            use_previous = bool(waiting_reason == "CrashLoopBackOff" or terminated_reason)
            try:
                text = self.core.read_namespaced_pod_log(
                    name=name, namespace=namespace, container=container_name,
                    previous=use_previous, tail_lines=80, timestamps=True,
                )
                result.append({"container": str(container_name), "source": "previous" if use_previous else "current", "text": _redact(str(text)[-4000:])})
            except Exception as exc:
                result.append({"container": str(container_name), "source": "unavailable", "text": f"Could not read logs: {type(exc).__name__}: {exc}"})
        return result

    def approve_restart(self, finding: dict[str, Any]) -> bool:
        """Prompt for exact per-controller approval, then patch restart annotation."""
        kind = finding.get("kind")
        namespace = finding.get("namespace")
        name = finding.get("name")
        if kind not in RESTARTABLE_KINDS or not namespace or not name:
            print("Refusing: only Deployment, StatefulSet, and DaemonSet restarts are supported.")
            return False
        recommendation = known_recommendation(finding)
        if recommendation["action"] != "restart_workload":
            print("Refusing: this finding has no recognized restart recommendation.")
            return False

        print("\nPROPOSED CHANGE")
        print(f"Target: {kind} {namespace}/{name}")
        print(f"Observed reason: {finding.get('reason')}")
        print(f"Evidence: {finding.get('message')}")
        print(f"Why this action: {recommendation['why']}")
        print("Impact: this triggers a rolling restart; it may disrupt traffic and is not guaranteed to fix the root cause.")
        expected = f"APPROVE {kind}/{name} in {namespace}"
        print(f"To proceed, type exactly: {expected}")
        try:
            response = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("No approval received; no change made.")
            return False
        if response != expected:
            print("Approval did not match; no change made.")
            return False

        timestamp = datetime.now(timezone.utc).isoformat()
        patch = {"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": timestamp}}}}}
        try:
            if kind == "Deployment":
                self.apps.patch_namespaced_deployment(name=name, namespace=namespace, body=patch)
            elif kind == "StatefulSet":
                self.apps.patch_namespaced_stateful_set(name=name, namespace=namespace, body=patch)
            else:
                self.apps.patch_namespaced_daemon_set(name=name, namespace=namespace, body=patch)
        except Exception as exc:
            print(f"Restart request failed: {type(exc).__name__}: {exc}")
            return False
        print("Restart requested. Re-run K-Agent to verify rollout and inspect new events/logs.")
        return True


def print_report(report: dict[str, Any]) -> None:
    print("\n=== K-Agent Kubernetes Health Report ===")
    print(f"Generated: {report['generated_at_utc']}")
    print(f"Scope: {report['scope']}")
    print("\nInventory:")
    for name, count in sorted(report["inventory"].items()):
        print(f"  {name}: {count}")
    issues = [f for f in report["findings"] if f.get("health") == "ISSUE"]
    print(f"\nFindings: {len(report['findings'])} total; {len(issues)} issues")
    for finding in issues:
        print(f"\n[{finding['kind']}] {finding.get('namespace')}/{finding['name']}")
        print(f"  Status/reason: {finding.get('reason')}")
        print(f"  Evidence: {finding.get('message')}")
        print(f"  Recommendation: {finding.get('recommendation', UNKNOWN_MESSAGE)}")
        for log in finding.get("log_excerpt", []):
            print(f"  Logs ({log['container']}, {log['source']}): {log['text'][:1000]}")
    print(f"\nWarning events: {len(report['warning_events'])}")
    for event in report["warning_events"][-20:]:
        print(f"  [{event['namespace']}] {event['reason']} {event['object']}: {event['message']}")
    if not issues:
        print("No unhealthy conditions were identified in the resources the current identity could read.")
    print("\nUnknown or unsupported cases:")
    if not issues or all(f.get("suggested_action") == "investigate_only" for f in issues):
        print(f"  {UNKNOWN_MESSAGE}")
    for limitation in report["limitations"]:
        print(f"NOTE: {limitation}")


def main() -> int:
    parser = argparse.ArgumentParser(description="K-Agent: conservative Kubernetes health and troubleshooting assistant")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--namespace", help="Inspect one namespace (default: all namespaces)")
    scope.add_argument("--all-namespaces", action="store_true", help="Explicitly inspect all namespaces")
    parser.add_argument("--watch", action="store_true", help="Repeat read-only inspection at a fixed interval")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds (minimum 5)")
    parser.add_argument("--no-logs", action="store_true", help="Do not read Pod logs")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--approve-restarts", action="store_true", help="Offer exact interactive approval for supported workload restarts")
    args = parser.parse_args()
    if args.interval < 5:
        parser.error("--interval must be at least 5 seconds")
    try:
        agent = KAgent(namespace=args.namespace)
    except Exception as exc:
        print(f"Unable to initialize Kubernetes client: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Check kubeconfig/context, cluster connectivity, and SDK installation.", file=sys.stderr)
        return 2

    try:
        while True:
            report = agent.inspect(include_logs=not args.no_logs)
            if args.json:
                print(json.dumps(report, indent=2, default=str))
            else:
                print_report(report)
            if args.approve_restarts:
                for finding in report["restart_candidates"]:
                    agent.approve_restart(finding)
            if not args.watch:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nK-Agent stopped by user.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
