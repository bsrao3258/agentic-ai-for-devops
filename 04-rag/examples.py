"""Introductory retrieval examples using only the Python standard library."""


RUNBOOKS = [
    {"id": "RUNBOOK-1", "tags": ["timeout", "network"], "text": "Check network path, server health, and latency."},
    {"id": "RUNBOOK-2", "tags": ["null pointer", "python"], "text": "Check variable initialization and recent code changes."},
    {"id": "RUNBOOK-3", "tags": ["permission denied", "access"], "text": "Verify identity, role, and least-privilege permissions."},
]


def retrieve(query: str) -> list[dict]:
    words = set(query.lower().split())
    ranked = []
    for doc in RUNBOOKS:
        tags = set(" ".join(doc["tags"]).lower().split())
        score = len(words & tags)
        if score:
            ranked.append((score, doc))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in ranked]


if __name__ == "__main__":
    for result in retrieve("Jenkins network timeout"):
        print(f"{result['id']}: {result['text']}")
