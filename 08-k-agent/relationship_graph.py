"""Evidence-based Kubernetes relationship helpers for K-Agent v2.

These pure functions operate on Kubernetes-style dictionaries so they can be
unit-tested without a cluster. They deliberately report relationships and
observations; they do not infer that a matching label proves application health.
"""
from __future__ import annotations

from typing import Any


def _value(obj: Any, snake: str, camel: str | None = None, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(snake, obj.get(camel or snake, default))
    return getattr(obj, snake, default)


def metadata(obj: Any) -> dict[str, Any]:
    return _value(obj, "metadata", default={}) or {}


def resource_name(obj: Any) -> str:
    return str(_value(metadata(obj), "name", default="unknown"))


def resource_namespace(obj: Any) -> str:
    return str(_value(metadata(obj), "namespace", default="default"))


def resource_labels(obj: Any) -> dict[str, str]:
    return _value(metadata(obj), "labels", default={}) or {}


def selector_matches(selector: dict[str, str], labels: dict[str, str]) -> bool:
    """Kubernetes Service selector semantics: every selector pair must match."""
    return bool(selector) and all(labels.get(key) == value for key, value in selector.items())


def service_pod_relationship(service: Any, pods: list[Any]) -> dict[str, Any]:
    """Match a Service selector to Pods in the same namespace and summarize readiness."""
    service_meta = metadata(service)
    spec = _value(service, "spec", default={}) or {}
    selector = _value(spec, "selector", default={}) or {}
    namespace = resource_namespace(service)
    matched = [
        pod for pod in pods
        if resource_namespace(pod) == namespace
        and selector_matches(selector, resource_labels(pod))
    ]
    ready_pods = []
    for pod in matched:
        status = _value(pod, "status", default={}) or {}
        conditions = _value(status, "conditions", default=[]) or []
        ready = any(
            _value(condition, "type") == "Ready"
            and str(_value(condition, "status", default="False")) == "True"
            for condition in conditions
        )
        if ready:
            ready_pods.append(resource_name(pod))
    return {
        "service": f"Service/{resource_name(service)}",
        "namespace": namespace,
        "selector": dict(selector),
        "selector_configured": bool(selector),
        "matched_pods": sorted(resource_name(pod) for pod in matched),
        "ready_pods": sorted(ready_pods),
        "matched_pod_count": len(matched),
        "ready_pod_count": len(ready_pods),
        "diagnosis": (
            "NO_SELECTOR" if not selector else
            "NO_MATCHING_PODS" if not matched else
            "MATCHED_PODS_NOT_READY" if not ready_pods else
            "READY_PODS_MATCH"
        ),
        "note": "Selector matches are evidence only; inspect EndpointSlices and application health before concluding traffic works.",
    }


def endpoint_summary(endpoints: Any) -> dict[str, Any]:
    """Summarize legacy Endpoints ready/not-ready addresses without guessing health."""
    subsets = _value(endpoints, "subsets", default=[]) or []
    ready: list[str] = []
    not_ready: list[str] = []
    for subset in subsets:
        for address in (_value(subset, "addresses", default=[]) or []):
            target = _value(address, "target_ref", "targetRef", default={}) or {}
            ready.append(str(_value(target, "name", default=_value(address, "ip", default="unknown"))))
        for address in (_value(subset, "not_ready_addresses", "notReadyAddresses", default=[]) or []):
            target = _value(address, "target_ref", "targetRef", default={}) or {}
            not_ready.append(str(_value(target, "name", default=_value(address, "ip", default="unknown"))))
    return {
        "endpoints": f"Endpoints/{resource_name(endpoints)}",
        "namespace": resource_namespace(endpoints),
        "ready_addresses": sorted(ready),
        "not_ready_addresses": sorted(not_ready),
        "ready_count": len(ready),
        "not_ready_count": len(not_ready),
        "diagnosis": "NO_READY_ENDPOINTS" if not ready else "READY_ENDPOINTS_PRESENT",
    }


def owner_references(obj: Any) -> list[dict[str, str]]:
    """Return declared owner references; this is one hop, not a verified full owner chain."""
    refs = _value(metadata(obj), "owner_references", "ownerReferences", default=[]) or []
    return [
        {
            "kind": str(_value(ref, "kind", default="Unknown")),
            "name": str(_value(ref, "name", default="unknown")),
            "uid": str(_value(ref, "uid", default="")),
            "controller": str(_value(ref, "controller", default="false")).lower(),
        }
        for ref in refs
    ]


def build_relationship_report(service: Any, pods: list[Any], endpoints: Any | None = None) -> dict[str, Any]:
    """Combine selector evidence, one-hop Pod ownership, and optional Endpoints evidence."""
    relationship = service_pod_relationship(service, pods)
    matched_names = set(relationship["matched_pods"])
    owners = []
    for pod in pods:
        if resource_namespace(pod) == relationship["namespace"] and resource_name(pod) in matched_names:
            owners.append({
                "pod": resource_name(pod),
                "owner_references": owner_references(pod),
            })
    report = {"service_relationship": relationship, "pod_ownership": owners}
    if endpoints is not None:
        report["endpoint_summary"] = endpoint_summary(endpoints)
    return report
