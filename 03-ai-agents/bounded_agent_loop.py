"""Example 2: a bounded, deterministic observe-decide-review loop.

This is an educational simulation, not an LLM agent and not an executor.
"""


def inspect(log_text: str) -> dict:
    text = log_text.lower()
    if "timeout" in text:
        return {"category": "TIMEOUT", "evidence": "timeout"}
    if "disk full" in text:
        return {"category": "DISK_FULL", "evidence": "disk full"}
    return {"category": "UNKNOWN", "evidence": "no known pattern"}


def propose_next_step(result: dict) -> str:
    suggestions = {
        "TIMEOUT": "Check network latency and upstream health.",
        "DISK_FULL": "Check filesystem usage with an approved read-only command.",
        "UNKNOWN": "Collect more sanitized logs before proposing a fix.",
    }
    return suggestions[result["category"]]


def run_agent(log_text: str, max_steps: int = 2) -> dict:
    # A small explicit limit helps demonstrate bounded workflows.
    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")
    observation = inspect(log_text)
    recommendation = propose_next_step(observation)
    return {
        "steps_used": 1,
        "step_limit": max_steps,
        "category": observation["category"],
        "recommendation": recommendation,
        "approval_required": True,
    }


if __name__ == "__main__":
    print(run_agent("Jenkins connection timeout"))
    print(run_agent("Node reports disk full"))
