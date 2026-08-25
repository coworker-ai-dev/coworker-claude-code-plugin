---
name: check-connectors
description: Default first step for any work-related session, not just ones that already look like they need company data. Find out who the current user is and which company data sources they can actually reach (Slack, Jira, GitHub, HubSpot, Salesforce, Google, BigQuery, Snowflake, etc.) before deciding whether other Coworker skills apply — you can't judge relevance to company context without first knowing what context is available. Also use whenever a data-source tool returns an auth/permission error. Calls the Coworker MCP `individual_context` tool.
---

# Check user context and connectors

Use the Coworker MCP `individual_context` tool to load the user's identity and data-source access.

## Procedure

1. Call `individual_context` early in any session where the topic could plausibly touch work — not only once a specific need is identified. It caches automatically, so this is a one-time, low-cost call per conversation.
2. Read `data_source_context` to see which connectors are accessible, blocked, or unavailable. Treat this as the baseline for what "relevant" can even mean in this session — you can't rule company context out if you don't know what's connected.
3. Only call connector tools for sources the user can reach. If a needed source is unavailable, tell the user and suggest connecting it in Coworker rather than failing silently.
4. Note any `custom_mcp_context` — the user may have additional connected MCP servers available as tools.

## Notes

- Use the returned role/team to personalize answers and pick sensible defaults (e.g. their team's Jira project).
- Running this early is what makes the lower-bar triggering in `ask-company` and `who-is` actually cheap — once identity/access is loaded, subsequent checks are fast, so there's less reason to gate them behind "is this obviously relevant."
