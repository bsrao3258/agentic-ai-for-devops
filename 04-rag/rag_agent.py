"""A tiny keyword lookup to introduce knowledge retrieval."""


KNOWLEDGE_BASE = [
    {
        "error": "timeout",
        "solution": "Check network connectivity, server health, and latency."
    },
    {
        "error": "null pointer",
        "solution": "Check variable initialization and recent code changes."
    },
]


def retrieve_solution(error_log):
    text = error_log.lower()
    for item in KNOWLEDGE_BASE:
        if item["error"] in text:
            return item["solution"]
    return "No known solution found. Inspect logs and gather more evidence."


if __name__ == "__main__":
    print(retrieve_solution("Connection timeout"))
