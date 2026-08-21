---
name: ask-company
description: Answer questions about THIS company — its decisions, policies, processes, projects, customers, teams, and "what do we know about X". Use whenever the user asks something that depends on internal/organizational knowledge rather than general or public information. Routes through the Coworker MCP (OM2 knowledge graph and connector search) instead of answering from priors.
---

# Ask the company

When a question depends on internal company knowledge, do NOT answer from prior knowledge — ground the answer in the company's own data via the Coworker MCP.

## The short version

1. Call `individual_context` once per session to learn who's asking and which data sources they can access.
2. Search the organizational memory knowledge graph first (`om2_search`, `om2_entity_search`, `om2_enumerate`, `om2_cypher`), then use connector-specific search for live detail.
3. Call `om2_identify_people` when people are named. Cite the source behind each claim; if Coworker returns nothing relevant, say so instead of guessing.

## The live playbook

The full current procedure — exact search order, fallbacks, and when to stop — is maintained server-side and may be newer than this file. Call `skill_retrieve` with skill name `mcp-company-data-cascade` and follow what it returns. For conflicting sources, exhaustive-page reads, timezones, freshness, or reading user-provided links — there's no fixed skill name for those; use `skill_search` to find the current task-specific playbook.
