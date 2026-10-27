# MCP — Line-by-Line Code Walkthrough

## Server example

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devops-learning-tools")

@mcp.tool()
def classify_log(log_text: str) -> dict:
    text = log_text.lower()
    if "timeout" in text:
        return {"category": "TIMEOUT", "suggestion": "Check network latency and server health."}
    return {"category": "UNKNOWN", "suggestion": "Collect more evidence."}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

- The import loads the FastMCP helper from the installed MCP Python SDK.
- `FastMCP("devops-learning-tools")` creates a server object with a human-readable name.
- `@mcp.tool()` registers the following function as a tool that compatible MCP clients can discover and call.
- `classify_log(log_text: str) -> dict` defines the tool, expects text, and returns structured data.
- `log_text.lower()` normalizes case.
- `if "timeout" in text:` selects a known timeout response.
- `return {...}` sends a result back to the MCP client; it does not fix anything.
- The fallback returns an unknown category when the pattern does not match.
- `if __name__ == "__main__":` ensures the server starts only when this file is run directly.
- `mcp.run(transport="stdio")` starts the server using standard input/output as the protocol transport. These streams are used for protocol messages, so avoid ordinary debug prints to stdout in a stdio server.

## Run it
Install the SDK inside the active virtual environment:
```powershell
python -m pip install "mcp[cli]"
python .\05-mcp\mcp_server.py
```
A stdio server usually waits for a compatible client; a silent terminal does not necessarily mean it is broken.

## Safety
This example only classifies supplied text. If a server later gains Jenkins, Kubernetes, cloud, or shell tools, validate inputs, use least-privilege identities, add timeouts and audit logs, and require explicit approval for state changes.

## Practice
Add a `severity` field to each result. Explain how a client would discover and call this tool.
