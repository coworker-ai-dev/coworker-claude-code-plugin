---
name: check-connectors
description: Find out who the current user is and which company data sources they can actually reach (Slack, Jira, GitHub, HubSpot, Salesforce, Google, BigQuery, Snowflake, etc.) before querying. Use at the start of a session, or whenever a data-source tool returns an auth/permission error, to avoid querying sources the user lacks access to. Calls the Coworker MCP individual_context tool.
---

# Check user context and connectors

Use the Coworker MCP `individual_context` tool to load the user's identity and data-source access.

## Procedure

1. Call `individual_context` early in the session (it caches automatically — once per conversation is enough).
2. Read `data_source_context` to see which connectors are accessible, blocked, or unavailable.
3. Only call connector tools for sources the user can reach. If a needed source is unavailable, tell the user and suggest connecting it in Coworker rather than failing silently.
4. Note any `custom_mcp_context` — the user may have additional connected MCP servers available as tools.

## Notes

- Use the returned role/team to personalize answers and pick sensible defaults (e.g. their team's Jira project).
