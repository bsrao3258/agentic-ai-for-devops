"""First DevOps log-analysis exercise: rule-based detection."""


def analyze_logs(logs):
    print("Analyzing DevOps logs...")
    print(logs)

    if "timeout" in logs.lower():
        print("Problem: Timeout error detected.")
        print("Suggestion: Check network latency and retry settings.")
    elif "null pointer" in logs.lower():
        print("Problem: Null pointer error detected.")
        print("Suggestion: Check variable initialization.")
    else:
        print("Problem: Unknown error.")
        print("Suggestion: Review logs for further investigation.")


if __name__ == "__main__":
    pipeline_log = """
    Jenkins pipeline failed.
    Error: Connection timeout while accessing the server.
    """
    analyze_logs(pipeline_log)
