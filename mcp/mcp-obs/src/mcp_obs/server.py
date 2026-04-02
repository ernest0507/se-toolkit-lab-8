"""Observability MCP server for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx


app = Server("mcp-obs")


def get_victorialogs_url() -> str:
    return os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")


def get_victoriatraces_url() -> str:
    return os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="logs_search",
            description="Search logs in VictoriaLogs by keyword and/or time range",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "LogsQL query string (e.g., '_time:10m service.name:\"Learning Management Service\" severity:ERROR')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="logs_error_count",
            description="Count errors per service over a time window",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_window": {
                        "type": "string",
                        "description": "Time window (e.g., '10m', '1h', '24h')",
                        "default": "1h",
                    },
                    "service": {
                        "type": "string",
                        "description": "Service name to filter by",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="traces_list",
            description="List recent traces for a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Service name to query traces for",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of traces to return",
                        "default": 10,
                    },
                },
                "required": ["service"],
            },
        ),
        Tool(
            name="traces_get",
            description="Fetch a specific trace by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "The trace ID to fetch",
                    },
                },
                "required": ["trace_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "logs_search":
        return await logs_search(arguments["query"], arguments.get("limit", 10))
    elif name == "logs_error_count":
        return await logs_error_count(
            arguments.get("time_window", "1h"), arguments.get("service", "")
        )
    elif name == "traces_list":
        return await traces_list(arguments["service"], arguments.get("limit", 10))
    elif name == "traces_get":
        return await traces_get(arguments["trace_id"])
    else:
        raise ValueError(f"Unknown tool: {name}")


async def logs_search(query: str, limit: int) -> list[TextContent]:
    url = f"{get_victorialogs_url()}/select/logsql/query"
    params = {"query": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.text
            return [TextContent(type="text", text=data)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching logs: {e}")]


async def logs_error_count(time_window: str, service: str) -> list[TextContent]:
    url = f"{get_victorialogs_url()}/select/logsql/query"
    if service:
        query = f'_time:{time_window} service.name:"{service}" severity:ERROR'
    else:
        query = f"_time:{time_window} severity:ERROR"
    params = {"query": query, "limit": 20}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.text
            return [TextContent(type="text", text=data)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error counting errors: {e}")]


async def traces_list(service: str, limit: int) -> list[TextContent]:
    url = f"{get_victoriatraces_url()}/select/jaeger/api/traces"
    params = {"service": service, "limit": limit}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            traces = data.get("data", [])
            if not traces:
                return [
                    TextContent(
                        type="text", text=f"No traces found for service: {service}"
                    )
                ]
            result = f"Found {len(traces)} traces for service '{service}':\n"
            for trace in traces[:5]:
                trace_id = (
                    trace["spans"][0]["traceID"] if trace.get("spans") else "unknown"
                )
                result += f"- Trace ID: {trace_id}\n"
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing traces: {e}")]


async def traces_get(trace_id: str) -> list[TextContent]:
    url = f"{get_victoriatraces_url()}/select/jaeger/api/traces/{trace_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            traces = data.get("data", [])
            if not traces:
                return [
                    TextContent(type="text", text=f"No trace found with ID: {trace_id}")
                ]
            trace = traces[0]
            result = f"Trace ID: {trace_id}\n"
            result += f"Service: {list(trace.get('processes', {}).values())[0].get('serviceName', 'unknown')}\n"
            result += f"Number of spans: {len(trace.get('spans', []))}\n\n"
            result += "Spans:\n"
            for span in trace.get("spans", []):
                name = span.get("operationName", "unknown")
                duration = span.get("duration", 0)
                result += f"  - {name} ({duration}μs)\n"
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching trace: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
