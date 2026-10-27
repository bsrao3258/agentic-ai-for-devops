"""Build and display a prompt; no external LLM API is called."""


def build_prompt(error_log):
    return f"""You are a DevOps troubleshooting assistant.

Analyze this error log:
{error_log}

Identify the likely problem, explain your reasoning, and recommend
safe investigation steps. Do not make changes to systems.
"""


if __name__ == "__main__":
    sample_log = "Connection timeout while accessing server"
    print(build_prompt(sample_log))
