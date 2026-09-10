#!/usr/bin/env python3
"""PreToolUse hook: tag each Coworker MCP call with this Claude Code session id.

The Coworker MCP endpoint is stateless (no Mcp-Session-Id), so on its own it
cannot tell one Claude Code conversation from another. Passing the session id
Claude Code already assigns this conversation (an opaque UUID) lets Coworker
keep one activity history per conversation. Nothing else is read or sent.

Any failure is a silent no-op: the tool call goes through unchanged.
"""
import json
import sys

try:
    hook = json.load(sys.stdin)
    session = hook.get("session_id")
    tool_input = hook.get("tool_input")
    if session and isinstance(tool_input, dict):
        tool_input["client_session_id"] = session
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": tool_input}}))
except Exception:
    pass
