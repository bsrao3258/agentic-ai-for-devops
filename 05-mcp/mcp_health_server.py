"""Example 2: MCP server with a read-only synthetic service-health tool.

Install: python -m pip install "mcp[cli]"
Run this server through an MCP-compatible client using stdio transport.
The values are sample data; this does not query real infrastructure.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devops-health-learning-tools")


@mcp.tool()
def get_sample_service_health(service_name: str) -> dict:
    """Return synthetic health information for a known demo service."""
    known_services = {
        "jenkins": {"status": "degraded", "last_check": "sample-data"},
        "payments-api": {"status": "healthy", "last_check": "sample-data"},
    }
    key = service_name.strip().lower()
    if key not in known_services:
        return {
            "service": service_name,
            "status": "unknown",
            "message": "No sample record exists; no live system was queried.",
        }
    return {"service": key, **known_services[key]}


if __name__ == "__main__":
    # MCP uses stdout for protocol messages; do not add print-based logging here.
    mcp.run(transport="stdio")
