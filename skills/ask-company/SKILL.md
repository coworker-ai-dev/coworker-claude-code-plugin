---
name: ask-company
description: Answer questions about THIS company — its decisions, policies, processes, projects, customers, teams, and "what do we know about X". Use whenever the user asks something that depends on internal/organizational knowledge rather than general or public information. Routes through the Coworker MCP (memory_retrieval, OM2 knowledge graph, and connector search) instead of answering from priors.
---

# Ask the company

When a question depends on internal company knowledge, do NOT answer from prior knowledge. Ground the answer in the company's own data via the Coworker MCP.

## Procedure

1. **Establish who's asking** (once per session): if you don't already have it, call `individual_context` to learn the user's role, team, and which data sources they can access. Don't query sources they can't reach.
2. **Pull organizational memory**: call `memory_retrieval` with a short query summarizing the question. This surfaces prior decisions, norms, and connector-specific knowledge.
3. **Use the knowledge graph when available**: if OM2 tools are present (e.g. `om2_search`), prefer `om2_search` for "what do we know about X / what happened with Y / summarize Z" — it expands across related facts, not just direct matches. See the `knowledge-graph` skill for which OM2 tool to pick.
4. **Resolve people**: if the question names people, call `identify_people` to get their real identity, role, and relationships.
5. **Drill into sources** only as needed: use the relevant connector search tool (Slack, Jira, GitHub, etc.) for specifics, scoped to sources the user can access.
6. **Cite**: name the source (doc, message, ticket, or entity) behind each claim. If OM2 is available, `om2_source_trace` can recover the supporting sources.

## Rules

- **OM2 first, not OM2 only:** lead with memory + the knowledge graph to orient, then chain to the connector for live/recent specifics. For the full ordering, retrieve the `company-data-cascade` skill with `skill_retrieve`.
- If the Coworker MCP returns nothing relevant, say so plainly rather than guessing.
- Never invent internal facts. Distinguish "the company's records say…" from your own reasoning.
