# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question 1: "What is the agentic loop?"**

2 + 2 = 4

The Agentic Loop refers to the core reasoning cycle that autonomous AI agents follow to accomplish tasks. It's typically described as:

1. Observe — Gather information about the current state (read files, check outputs, recall context)
2. Think/Reason — Analyze the situation, plan next steps, consider alternatives
3. Act — Execute actions using available tools (write files, run commands, call APIs, send messages)
4. Reflect — Evaluate the results, detect errors, adjust the plan

This loop repeats until the goal is achieved or the agent determines it cannot proceed.

**Question 2: "What labs are available in our LMS?"**

Based on my exploration of the workspace, here are the **available labs** in your LMS:

## Required Tasks (Lab 8)
The current lab is Lab 8 - "The Agent is the Interface" which focuses on AI agents as client interfaces. It has 5 required tasks:

1. Task 1 — Set Up the Agent (Parts A, B, C)
2. Task 2 — Deploy the Agent and Add a Web Client (Parts A, B)
3. Task 3 — Give the Agent New Eyes (Observability) (Parts A, B, C)
4. Task 4 — Diagnose a Failure and Make the Agent Proactive (Parts A, B, C)
5. Task 5 — (listed in directory, details in task file)

## Optional Task
- Task 1 — Add a Telegram Bot Client

(Note: Without MCP tools, the agent searched local repo files instead of querying real LMS data)

## Task 1B — Agent with LMS tools

**Question 1: "What labs are available?"**

Here are the available labs in the LMS:

| ID | Lab Title |
|----|-----------|
| 1 | Lab 01 – Products, Architecture & Roles |
| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
| 4 | Lab 04 — Testing, Front-end, and AI Agents |
| 5 | Lab 05 — Data Pipeline and Analytics Dashboard |
| 6 | Lab 06 — Build Your Own Agent |
| 7 | Lab 07 — Build a Client with an AI Coding Agent |
| 8 | lab-08 |

**Question 2: "Is the LMS backend healthy?"**

Yes, the LMS backend is healthy. It currently has 56 items in the system.

## Task 1C — Skill prompt

**Question: "Show me the scores"**

There are 8 labs available. Which lab would you like to see the scores for? Here are the options:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you'd like to see scores for, or I can show you pass rates for all of them.

## Task 2A — Deployed agent

**Nanobot startup log excerpt:**

```
Using config: /app/nanobot/config.resolved.json
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
2026-03-31 22:10:43.816 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
2026-03-31 22:10:46.162 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
2026-03-31 22:10:48.252 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
2026-03-31 22:10:48.252 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

**WebSocket test via curl:**

```
Here are the available labs:

1. **Lab 01** – Products, Architecture & Roles
2. **Lab 02** — Run, Fix, and Deploy a Backend Service
3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy
4. **Lab 04** — Testing, Front-end, and AI Agents
5. **Lab 05** — Data Pipeline and Analytics Dashboard
6. **Lab 06** — Build Your Own Agent
7. **Lab 07** — Build a Client with an AI Coding Agent
8. **Lab 08** — lab-08

Would you like me to get more details about any specific lab, such as pass rates, completion rates, top learners, or submission timeline?
```

## Task 2B — Web client

**Flutter web app accessible at:** `http://<vm-ip>:42002/flutter/`

**WebSocket test results:**

Test 1 - "What can you do in this system?"
```
I can help you with querying the LMS (Learning Management System) for information about:
- Available labs and their details
- Pass rates and completion rates
- Submission timelines
- Group performance
- Top learners
- Learner information

I can also help you with general questions, but my primary strength is working with the LMS data to provide insights about your courses and student performance.
```

Test 2 - "How is the backend doing?"
```
The LMS backend is healthy. It currently has 56 items in the system.

The backend has been running normally with:
- Successful authentication
- Database queries executing properly
- Request completion with 200 status
```

Test 3 - "Show me the scores" (without specifying a lab)
```
There are 8 labs available. Which lab would you like to see the scores for? Here are the options:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you'd like to see scores for, or I can show you pass rates for all of them.
```

The Flutter web client:
- Shows login screen at `/flutter`
- Accepts access key: `nanobot_secret_pass`
- Successfully connects via WebSocket to `ws://localhost:42002/ws/chat?access_key=nanobot_secret_pass`
- Agent uses real LMS backend tools (not just generic responses)
- When asking "Show me the scores" without a lab, the agent asks user to choose from the available labs (structured choice behavior via mcp-webchat)

## Task 3A — Structured logging

**Happy-path log excerpt (showing request_started → request_completed with status 200):**

```
backend-1  | 2026-03-31 22:10:58,313 INFO [lms_backend.main] [main.py:62] [trace_id=a91cbe4fba7f02410da420803c179f76 span_id=46558895ca0a27f7 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 22:10:58,412 INFO [lms_backend.auth] [auth.py:30] [trace_id=a91cbe4fba7f02410da420803c179f76 span_id=46558895ca0a27f7 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 22:10:58,448 INFO [lms_backend.db.items] [items.py:16] [trace_id=a91cbe4fba7f02410da420803c179f76 span_id=46558895ca0a27f7 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-31 22:10:58,747 INFO [lms_backend.main] [main.py:74] [trace_id=a91cbe4fba7f02410da420803c179f76 span_id=46558895ca0a27f7 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.20.0.9:58728 - "GET /items/ HTTP/1.1" 200 OK
```

**Error-path log excerpt (showing db_query with error):**

```
backend-1  | 2026-03-31 22:12:47,153 ERROR [lms_backend.db.items] [items.py:23] [trace_id=c4510077b85de973604ac1b8a9cb7443 span_id=11e1e3d76e47e0fe resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-31 22:12:49,872 ERROR [lms_backend.db.items] [items.py:23] [trace_id=578b76520ed78245731d7292c0e5ad17 span_id=700a7d56d6a41953 resource.service.name=Learning Management Service trace_sampled=True] - db_query
```

These errors occurred when PostgreSQL was stopped, causing database connection failures.

**VictoriaLogs query:**
- URL: `http://<vm-ip>:42002/utils/victorialogs/select/vmui`
- Query: `_time:1h service.name:"Learning Management Service" severity:ERROR`
- Result: Shows error logs with trace_id, span_id, and event details

The structured logging includes fields: `trace_id`, `span_id`, `service.name`, `severity`, `event` which can be filtered in VictoriaLogs.

## Task 3B — Traces

**VictoriaTraces UI:** `http://<vm-ip>:42002/utils/victoriatraces`

**Healthy trace example:**
- Trace ID: `ca17126e7bac1c65a94f1694063befc6`
- Service: Learning Management Service
- Spans:
  - `request_started` → `auth_success` → `db_query` → `request_completed`
  - HTTP GET /items/ with status 200
- Span hierarchy shows the request flow through authentication and database query

**Error trace example (PostgreSQL down):**
- Trace ID: `578b76520ed78245731d7292c0e5ad17`
- Service: Learning Management Service
- Spans:
  - `GET /items/ http send` shows `http.status_code: 404`
  - The error occurs in the `db_query` span
- The trace shows where the failure happened (database connection failure)

**VictoriaTraces API examples:**
```
GET http://victoriatraces:10428/select/jaeger/api/traces?service=Learning%20Management%20Service&limit=5
GET http://victoriatraces:10428/select/jaeger/api/traces/578b76520ed78245731d7292c0e5ad17
```

The traces show the full span hierarchy with timing information for each step of the request processing.

## Task 3C — Observability MCP tools

**Test 1: Normal conditions - "Any LMS backend errors in the last 10 minutes?"**

```
Good news! **No LMS backend errors** in the last 10 minutes. 

The LMS backend is currently **healthy** with 56 items in the system. I also checked for any errors across all services in that time window and found none.
```

**Test 2: Failure conditions (PostgreSQL stopped) - "Any LMS backend errors in the last 10 minutes?"**

```
Yes, there are **3 errors** in the LMS backend in the last 10 minutes. All are database-related:

**Error Types:**
1. **DNS Resolution Failure** (2 occurrences): `[Errno -2] Name or service not known` - The service cannot resolve the database hostname
2. **Connection Closed** (1 occurrence): `asyncpg.exceptions.InterfaceError: connection is closed` - Database connection was unexpectedly closed

**Impact:** These errors are affecting database queries on the `item` table, which could cause LMS features to fail.

**Trace IDs** for further investigation:
- `8eca139ecccc6f24bd06067dd77ab8f9`
- `96910c252a0b7c71a36390064b8a87a5`
- `b32af10f0d2570f5531f2acb5bca0ea9`

The DNS errors suggest a network/configuration issue with the database connection. Would you like me to fetch more details from any of these traces?
```

**MCP tools registered:**
- `mcp_obs_logs_search`
- `mcp_obs_logs_error_count`
- `mcp_obs_traces_list`
- `mcp_obs_traces_get`

## Task 4A — Multi-step investigation

**Question: "What went wrong?" (with PostgreSQL stopped)**

The agent performed the investigation flow:
1. `logs_error_count` with time_window="5m" 
2. `logs_search` for errors in LMS service
3. `traces_get` for trace ID

**Response:**
```
## What Went Wrong

**The Learning Management Service (LMS) backend is failing to connect to its database.**

### Error Details:
- **Error Type**: Database connection failure
- **Impact**: The LMS backend cannot reach PostgreSQL
- **Trace ID**: 2a291736e8084038040d50d0b6c7be50

The investigation found database connection errors in the logs and the corresponding trace shows the failure in the db_query span.
```

The agent correctly identified the root cause (PostgreSQL connection failure) and cited both log evidence and trace evidence.

## Task 4B — Proactive health check

**Created health check via cron tool:**

The agent successfully created a cron job running every 2 minutes:
- Job ID: f328a909
- Name: LMS Health Check
- Schedule: Every 2 minutes

**First cron run (22:31 UTC) - UNHEALTHY:**
```
**🏥 LMS Health Check** (22:31 UTC)

⚠️ **UNHEALTHY** - Errors detected in last 2 minutes

**Issue:** Database connection failure in the LMS backend
```

**Second cron run (22:33 UTC) - healthy:**
After the 2-minute window passed with fresh errors, it reported:
```
🐱 **LMS Health Check** — System is healthy!

No errors detected in the Learning Management Service over the last 2 minutes.
```

The cron job successfully:
1. Uses `logs_error_count` to check for errors in the last 2 minutes
2. Posts proactive health reports to the same chat
3. Reports unhealthy when errors are detected, healthy when no recent errors

## Task 4C — Bug fix and recovery

**1. Root cause identified:**

The planted bug was in `backend/src/lms_backend/routers/items.py`. When the database query failed (e.g., PostgreSQL was down), the code was catching all exceptions and converting them to a misleading `404 Not Found` response:

```python
except Exception as exc:
    logger.warning(
        "items_list_failed_as_not_found",
        extra={"event": "items_list_failed_as_not_found"},
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Items not found",
    ) from exc
```

This hid the real database error behind a fake "not found" message.

**2. Fix applied:**

Changed the error handling to properly propagate the actual error:

```python
except Exception as exc:
    logger.error(
        "items_list_failed",
        extra={"event": "items_list_failed", "error": str(exc)},
    )
    raise
```

Now when PostgreSQL is down, the actual error (`[Errno -2] Name or service not known`) is returned instead of the misleading `404 Items not found`.

**3. Post-fix failure check:**

After redeploying with the fix, when PostgreSQL was stopped:
- Request to `/items/` now returns the real error: `"detail":"[Errno -2] Name or service not known"`
- The agent's "What went wrong?" investigation now shows the actual database connection error

**4. Healthy follow-up report:**

After restarting PostgreSQL, the cron job reported:
```
🐾 **Health Check Report**

System looks healthy! No backend errors detected in the last 2 minutes.
```

The system now properly reports database errors instead of masking them as "not found".
