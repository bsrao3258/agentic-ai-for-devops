"""Reusable rule-based DevOps log classifier."""


def classify_error(logs):
    text = logs.lower()

    if "timeout" in text:
        return "TIMEOUT"
    elif "null pointer" in text:
        return "NULL_POINTER"
    return "UNKNOWN"


def get_recommendation(error_type):
    recommendations = {
        "TIMEOUT": "Check network connectivity, latency, and server health.",
        "NULL_POINTER": "Check variable initialization and recent code changes.",
        "UNKNOWN": "Inspect the logs and gather more evidence.",
    }
    return recommendations[error_type]


if __name__ == "__main__":
    sample = "Jenkins pipeline failed: connection timeout"
    error = classify_error(sample)
    print("Error type:", error)
    print("Recommendation:", get_recommendation(error))
    print("Approval required before applying any fix.")
