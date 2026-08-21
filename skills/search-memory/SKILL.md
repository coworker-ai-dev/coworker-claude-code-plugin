---
name: search-memory
description: Find past decisions, learnings, conventions, and connector knowledge stored in the company's organizational memory. Use when the user references something the team "decided", "agreed", "always does", or asks "have we done X before / what's our convention for Y". Calls the Coworker MCP memory_retrieval tool.
---

# Search organizational memory

Use the Coworker MCP `memory_retrieval` tool to recover stored organizational knowledge: decisions, norms, processes, and connector-specific insights (Slack/Jira/GitHub/Salesforce/etc.).

## Procedure

1. Call `memory_retrieval` with a focused `query` describing exactly what you're looking for (one concept at a time works best).
2. If results are thin, broaden or rephrase the query once before falling back to connector search.
3. Re-query whenever the topic shifts to a new area.

## Notes

- Memories come scoped as user-level or network-level — prefer network-level for shared conventions.
- To store something for the future, only use `memory_learning`, and only when the user explicitly asks you to remember it.
- If results conflict with each other or look stale, use `skill_search` to find the current data-quality playbook — there's no fixed skill name for it.
