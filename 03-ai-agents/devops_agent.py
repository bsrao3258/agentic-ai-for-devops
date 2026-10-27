"""Starter decision flow for a DevOps troubleshooting assistant."""


def devops_agent(error_log):
    error = error_log.lower()

    if "timeout" in error:
        recommendation = "Check network latency and retry settings."
    elif "null pointer" in error:
        recommendation = "Check variable initialization and recent changes."
    else:
        recommendation = "Review logs and gather more evidence."

    print("Recommendation:", recommendation)
    print("Human approval is required before applying any fix.")


if __name__ == "__main__":
    devops_agent("Connection timeout while accessing the server")
