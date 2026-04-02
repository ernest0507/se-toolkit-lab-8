#!/usr/bin/env python3
"""Entry point for nanobot in Docker. Resolves env vars into config.json and starts gateway."""

import json
import os
import sys


def resolve_config():
    config_path = "/app/nanobot/config.json"
    resolved_path = "/app/nanobot/config.resolved.json"

    with open(config_path, "r") as f:
        config = json.load(f)

    # Resolve LLM provider settings from env vars
    llm_api_key = os.environ.get("LLM_API_KEY", "")
    llm_api_base = os.environ.get("LLM_API_BASE_URL", "")
    llm_model = os.environ.get("LLM_API_MODEL", "")

    if "providers" in config and "custom" in config["providers"]:
        if llm_api_key:
            config["providers"]["custom"]["apiKey"] = llm_api_key
        if llm_api_base:
            config["providers"]["custom"]["apiBase"] = llm_api_base

    if "agents" in config and "defaults" in config["agents"]["defaults"]:
        if llm_model:
            config["agents"]["defaults"]["model"] = llm_model

    # Resolve gateway host/port from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")

    if "gateway" in config:
        config["gateway"]["host"] = gateway_host
        config["gateway"]["port"] = int(gateway_port)

    # Resolve MCP server settings for LMS
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")

    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            lms_config = config["tools"]["mcpServers"]["lms"]
            if "env" not in lms_config:
                lms_config["env"] = {}
            if lms_backend_url:
                lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
            if lms_api_key:
                lms_config["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

        # Add webchat MCP server
        mcp_webchat_url = os.environ.get(
            "NANOBOT_WEBCHAT_UI_RELAY_URL", "http://localhost:8765"
        )
        mcp_webchat_token = os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_TOKEN", "")

        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "MCP_WEBCHAT_URL": mcp_webchat_url,
                "MCP_WEBCHAT_TOKEN": mcp_webchat_token,
            },
        }

        # Add observability MCP server
        victorialogs_url = os.environ.get(
            "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
        )
        victoriatraces_url = os.environ.get(
            "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"
        )

        config["tools"]["mcpServers"]["obs"] = {
            "command": "python",
            "args": ["-m", "mcp_obs"],
            "env": {
                "NANOBOT_VICTORIALOGS_URL": victorialogs_url,
                "NANOBOT_VICTORIATRACES_URL": victoriatraces_url,
            },
        }

    # Enable webchat channel
    if "channels" not in config:
        config["channels"] = {}
    config["channels"]["webchat"] = {"enabled": True, "allowFrom": ["*"]}

    # Resolve webchat host/port
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")

    if "channels" in config and "webchat" in config["channels"]:
        config["channels"]["webchat"]["host"] = webchat_host
        config["channels"]["webchat"]["port"] = int(webchat_port)

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return resolved_path


def main():
    resolved_config = resolve_config()
    workspace = "/app/nanobot/workspace"

    os.execvp(
        "nanobot",
        ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace],
    )


if __name__ == "__main__":
    main()
