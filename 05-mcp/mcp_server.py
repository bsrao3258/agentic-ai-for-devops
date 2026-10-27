"""Minimal local MCP server exposing a safe log-classification tool.

Install: python -m pip install "mcp[cli]"
Run: python 05-mcp/mcp_server.py

This server classifies supplied text only; it does not access infrastructure.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devops-learning-tools")


@mcp.tool()
def classify_log(log_text: str) -> dict:
    """Classify a supplied log message and suggest safe next checks."""
    text = log_text.lower()
    if "timeout" in text:
        return {
            "category": "TIMEOUT",
            "suggestion": "Check network latency and server health.",
            "action": "read_only_investigation",
        }
    if "null pointer" in text:
        return {
            "category": "NULL_POINTER",
            "suggestion": "Check variable initialization and recent changes.",
            "action": "read_only_investigation",
        }
    return {
        "category": "UNKNOWN",
        "suggestion": "Collect more evidence and inspect surrounding logs.",
        "action": "read_only_investigation",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
