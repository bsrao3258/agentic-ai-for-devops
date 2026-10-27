# 05 — Model Context Protocol (MCP)

## What MCP provides
MCP is a protocol for exposing tools and other context to compatible AI applications through a standardized client/server interface. It is not itself an LLM and does not automatically make a tool safe.

## Architecture concepts
- **MCP host/client:** the AI application and its connection to a server.
- **MCP server:** exposes declared tools, resources, or prompts.
- **Tool:** a named operation with a schema for inputs and structured results.
- **Transport:** how client and server communicate.

## Example use case
A DevOps MCP server might expose read-only tools such as `get_pipeline_status`, `search_sanitized_logs`, or `get_deployment_summary`. State-changing operations should be separate, narrowly scoped, audited, and protected by explicit approval.

## SDK example
The file `mcp_server.py` contains a minimal server using the official Python MCP SDK. Install its dependency in your virtual environment before running it:

```powershell
python -m pip install "mcp[cli]"
python .\05-mcp\mcp_server.py
```
Linux:
```bash
python -m pip install "mcp[cli]"
python ./05-mcp/mcp_server.py
```
The server uses stdio transport. It is intended for local learning and should be connected to an MCP-compatible client; launching it may appear to wait silently because protocol messages use standard input/output.

## Security checklist
- Expose only necessary tools.
- Validate all inputs and enforce timeouts.
- Use least-privilege credentials and never hardcode secrets.
- Do not pass arbitrary shell commands from model text to a shell.
- Redact secrets from tool results.
- Confirm authorization for any state-changing operation.

## Exercises
1. Add a read-only tool that classifies a supplied log string.
2. Return structured JSON-like results with a severity field.
3. Write down which identity and permissions a real CI tool would need.
4. Design an approval workflow before adding a restart tool.

## Interview questions
- What are MCP host, client, server, and tool?
- How is MCP different from direct REST API integration?
- Why is tool input validation important?
- How would you protect an MCP server that can reach production?
