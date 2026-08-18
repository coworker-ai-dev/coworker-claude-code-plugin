---
name: knowledge-graph
description: Explore the company's OM2 organizational knowledge graph — the fastest way to understand people, projects, customers, and how they connect. Use for open-ended "what do we know about X", "how is A related to B", "what's the history of Y", or "what are the themes around Z" questions. Only applies when OM2 tools (om2_*) are available in this session; if they aren't, the network hasn't enabled OM2 — fall back to memory_retrieval and connector search.
---

# Organizational knowledge graph (OM2)

OM2 is a graph built from the company's connected data. It finds facts that are *indirectly* connected to your query, so it beats single-source search for understanding context. Use it before falling back to per-connector tools when the question is about organizational knowledge.

**You never look up an internal ID.** Every tool takes a name or a plain-language query and resolves entities server-side. Refer to OM2 as "organizational memory" and never expose internal node/report IDs to the user.

## Get the live guide first

The full, current usage guide — tool selection, procedure, result semantics, completeness/pagination signals, cypher recipes, anti-loop rules — is maintained server-side and may be newer than this file. Before any non-trivial graph work, call `skill_retrieve` with skill name `mcp-om2-usage` and follow what it returns.

## Quick tool map

- **`om2_search`** — default entry for open questions. Ranked top-K, not exhaustive.
- **`om2_entity_brief`** — the user named a specific account, deal, or contact.
- **`om2_entity_search`** — locate a person, project, or document by name.
- **`om2_enumerate`** — completeness questions ("all / every / list all").
- **`om2_source_trace`** — recover the source behind a fact, to cite or verify.
- **`om2_hybrid_search`** — may not be indexed yet; checks the live source with the user's permissions.
- **`om2_graph_schema` + `om2_cypher`** — bespoke graph-shaped questions the tools above don't cover.

## If OM2 tools are absent

The network hasn't enabled OM2 (the `enableOM2` flag is off). Don't claim graph results — use `memory_retrieval` and connector search instead.
