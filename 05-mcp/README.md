# 05 — Model Context Protocol (MCP)

## What MCP provides
MCP is a protocol for exposing tools and other context to compatible AI applications through a standardized client/server interface. It is not an LLM and does not automatically make a tool safe.

## Concepts
- **Host/client:** the AI application and its connection to a server.
- **Server:** exposes declared tools, resources, or prompts.
- **Tool:** a named operation with a defined input schema and result.
- **Transport:** how client and server communicate.

## Example use case
A DevOps server could expose read-only tools such as `get_pipeline_status`, `search_sanitized_logs`, or `get_deployment_summary`. State-changing operations need narrow scope, audit, and explicit approval.

## Run the learning server
Install the official SDK in your activated virtual environment:
```powershell
python -m pip install "mcp[cli]"
python .\05-mcp\mcp_server.py
```
Linux:
```bash
python -m pip install "mcp[cli]"
python ./05-mcp/mcp_server.py
```
The server uses stdio transport and is meant to be launched by an MCP-compatible client. It may wait silently while protocol messages are exchanged over stdin/stdout.

## Security checklist
Expose only necessary tools; validate inputs; use least-privilege credentials; never pass arbitrary model text to a shell; redact tool results; obtain approval for state changes.

## Exercises
Add a read-only classifier tool, return structured severity, describe required identity permissions, and design an approval gate before any restart tool.

## Interview questions
What are MCP host/client/server/tools? How does MCP differ from direct REST integration? Why validate tool input? How would you secure a server that can reach production?
