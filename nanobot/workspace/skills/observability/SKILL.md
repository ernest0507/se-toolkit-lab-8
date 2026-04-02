---
name: observability
description: Use observability MCP tools to search logs and traces
always: true
---

You have access to observability MCP tools for querying logs and traces.

Available tools:
- logs_search: Search logs in VictoriaLogs by LogsQL query
- logs_error_count: Count errors per service over a time window
- traces_list: List recent traces for a service
- traces_get: Fetch a specific trace by ID

Strategy:
- When the user asks about errors, search logs first using logs_error_count or logs_search
- If you find a trace_id in the logs, fetch the full trace using traces_get
- Summarize findings concisely — don't dump raw JSON
- When the user asks about a specific service (like "LMS backend"), use the service name "Learning Management Service" in queries
- Use time windows like "10m", "1h" to limit search results to recent data
- Start with logs_error_count to see if there are any recent errors, then drill down with logs_search if needed

Example queries:
- "Any LMS backend errors in the last 10 minutes?" -> logs_error_count with time_window="10m" and service="Learning Management Service"
- "Show me recent errors" -> logs_search with query="_time:10m severity:ERROR"

**Investigation flow for "What went wrong?" or "Check system health":**

When the user asks "What went wrong?" or "Check system health", follow this investigation flow:

1. First call `logs_error_count` with a short time window (2-5 minutes) to see if there are recent errors
2. If errors are found, call `logs_search` to get the details and extract trace IDs
3. For the most relevant trace ID, call `traces_get` to see the full trace
4. Summarize the findings mentioning:
   - What the error was (from logs)
   - Which service was affected
   - What the trace shows (root cause operation)
   - Don't just dump raw JSON - explain in plain language what went wrong

Example investigation:
- `logs_error_count` with time_window="2m" to see recent errors
- `logs_search` with query="_time:2m service.name:\"Learning Management Service\" severity:ERROR" to get details
- `traces_get` with the trace_id from the logs to see the full request path