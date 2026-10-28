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

## Additional example: read-only synthetic health tool

A second example server is available in [mcp_health_server.py](mcp_health_server.py). It exposes a `get_sample_service_health` tool for synthetic demo records. It does not contact real services.

Install the SDK in your activated virtual environment if you have not already:

```bash
python -m pip install "mcp[cli]"
```

Launch it through an MCP-compatible client configured for stdio transport. Like the first server, it may wait silently because stdout is reserved for MCP protocol messages. Do not test it by expecting ordinary terminal output, and do not add print-based logging to the protocol stream.

Try the tool with `jenkins`, `payments-api`, and an unknown service name. The first two return sample statuses; the unknown name returns an explicit unknown status. The server has not been verified against your local MCP client setup, so use the SDK's compatible client configuration for your environment.

## Visual: MCP client and server

MCP standardizes how a client discovers and calls server capabilities; authorization and safe tool design are still required.

```mermaid
flowchart LR
    A[AI host application] <--> B[MCP client]
    B <--> C[MCP server]
    C --> D[Declared tool schema]
    D --> E[Validate inputs]
    E --> F[Run narrow, permitted operation]
    F --> G[Structured result]
```
