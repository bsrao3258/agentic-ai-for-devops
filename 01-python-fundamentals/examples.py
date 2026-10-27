"""Runnable examples for the Python fundamentals module."""


def classify(logs: str) -> str:
    text = logs.lower()
    if "timeout" in text:
        return "TIMEOUT"
    elif "null pointer" in text:
        return "NULL_POINTER"
    elif "permission denied" in text:
        return "PERMISSION_DENIED"
    return "UNKNOWN"


def recommendation(error_type: str) -> str:
    suggestions = {
        "TIMEOUT": "Check network latency, server health, and retry settings.",
        "NULL_POINTER": "Check variable initialization and recent code changes.",
        "PERMISSION_DENIED": "Check identity, role, and least-privilege permissions.",
        "UNKNOWN": "Collect more evidence and inspect surrounding log lines.",
    }
    return suggestions[error_type]


if __name__ == "__main__":
    samples = [
        "Jenkins connection TIMEOUT",
        "Null pointer exception",
        "Permission denied while reading artifact",
        "Disk quota exceeded",
    ]
    for sample in samples:
        result = classify(sample)
        print(f"Input: {sample}")
        print(f"Class: {result}")
        print(f"Suggestion: {recommendation(result)}")
        print("-" * 40)
