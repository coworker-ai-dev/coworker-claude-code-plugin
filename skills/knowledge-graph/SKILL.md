---
name: knowledge-graph
description: Explore the company's OM2 organizational knowledge graph — the fastest way to understand people, projects, customers, and how they connect. Use for open-ended "what do we know about X", "how is A related to B", "what's the history of Y", or "what are the themes around Z" questions. Only applies when OM2 tools (om2_*) are available in this session; if they aren't, the network hasn't enabled OM2 — fall back to memory_retrieval and connector search.
---

# Organizational knowledge graph (OM2)

OM2 is a graph built from the company's connected data. It finds facts that are *indirectly* connected to your query, so it beats single-source search for understanding context. Use it before falling back to per-connector tools when the question is about organizational knowledge.

For the full tool-selection guide (completeness/pagination signals, search modes, anti-loop rules), retrieve the `mcp-om2-usage` skill from Coworker with `skill_retrieve`.

## Pick the right tool

- **`om2_search`** — default entry point. Semantic search with graph expansion. Best for "what do we know about X?", "what happened with Y?", "summarize Z". Keep each query focused on ONE concept.
- **`om2_entity_search`** — find a specific known entity (person, project, account) by name.
- **`om2_entity_brief`** — concise briefing on one entity before going deeper.
- **`om2_explore_neighbors` / `om2_find_path`** — see what an entity connects to, or how two entities relate.
- **`om2_person_network`** — a person's working network.
- **`om2_entity_timeline` / `om2_recent_activity`** — how something evolved over time / what's happened lately.
- **`om2_themes`** — recurring topics and narrative lanes across the graph.
- **`om2_source_trace`** — recover the source documents/messages behind a fact (use to cite or verify).

## Procedure

1. Start broad with `om2_search`. Read the connected facts it returns.
2. Narrow with `om2_entity_search` / `om2_entity_brief` on the specific entities that matter.
3. Expand relationships with `om2_explore_neighbors` or `om2_find_path` when the question is relational.
4. Always be ready to back a claim with `om2_source_trace`.

## If OM2 tools are absent

The network hasn't enabled OM2 (the `enableOM2` flag is off). Don't claim graph results — use `memory_retrieval` and connector search instead.
