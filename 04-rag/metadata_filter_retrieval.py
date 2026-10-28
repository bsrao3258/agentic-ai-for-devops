"""Example 2: retrieve approved runbooks using tags and metadata.

This is keyword/tag retrieval, not embeddings or vector search.
"""

RUNBOOKS = [
    {"id": "RB-101", "service": "jenkins", "approved": True,
     "tags": ["timeout", "network"], "text": "Check DNS, network path, and upstream health."},
    {"id": "RB-102", "service": "kubernetes", "approved": True,
     "tags": ["crashloop", "pod"], "text": "Inspect pod events and previous container logs."},
    {"id": "RB-999", "service": "jenkins", "approved": False,
     "tags": ["timeout"], "text": "Unreviewed draft; do not use for production."},
]


def retrieve(query: str, service: str) -> list[dict]:
    words = set(query.lower().split())
    results = []
    for doc in RUNBOOKS:
        if not doc["approved"] or doc["service"] != service:
            continue
        searchable = set(doc["tags"]) | set(doc["text"].lower().split())
        score = len(words & searchable)
        if score:
            results.append((score, doc))
    results.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in results]


if __name__ == "__main__":
    for item in retrieve("jenkins timeout network", "jenkins"):
        print(f"{item['id']} (approved={item['approved']}): {item['text']}")
