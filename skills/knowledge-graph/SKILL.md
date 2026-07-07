---
name: knowledge-graph
description: Explore the company's OM2 organizational knowledge graph — the fastest way to understand people, projects, customers, and how they connect. Use for open-ended "what do we know about X", "how is A related to B", "what's the history of Y", or "what are the themes around Z" questions. Only applies when OM2 tools (om2_*) are available in this session; if they aren't, the network hasn't enabled OM2 — fall back to memory_retrieval and connector search.
---

# Organizational knowledge graph (OM2)

OM2 is a graph built from the company's connected data. It finds facts that are *indirectly* connected to your query, so it beats single-source search for understanding context. Use it before falling back to per-connector tools when the question is about organizational knowledge.

**You never look up an internal ID.** Every tool takes a name or a plain-language query and resolves entities server-side. Refer to OM2 as "organizational memory" and never expose internal node/report IDs to the user.

For the full tool-selection guide (completeness/pagination signals, search modes, cypher recipes, anti-loop rules), retrieve the `mcp-om2-usage` skill from Coworker with `skill_retrieve`.

## Pick the right tool

- **`om2_search`** — default entry point. Semantic search with graph expansion. Best for "what do we know about X?", "what happened with Y?", "summarize Z". Keep each query focused on ONE concept. Ranked top-K, **not** exhaustive.
- **`om2_entity_brief`** — when the user names a specific account, deal, or contact. Assembles the customer + its deals + connected contacts from real relationships. Pass the user's phrasing as the text argument; use this instead of `om2_search` for a named account/deal.
- **`om2_entity_search`** — locate a specific person, project, or document by name.
- **`om2_enumerate`** — completeness questions ("find all / every / list all X that mention Y"). Returns the full deduplicated set, unlike `om2_search`.
- **`om2_source_trace`** — recover the source report/document behind a fact, to cite or verify.
- **`om2_hybrid_search`** — find something that may not be indexed yet; checks the live source with the user's real permissions.

**Power path (graph-shaped questions the tools above don't cover):** call `om2_graph_schema` to see this network's node/edge shape, then write a read-only query with `om2_cypher` (results are auto-restricted to what the user can see). Match entities by name/property in the query itself.

## Resolved entities come back to you

`om2_search`, `om2_entity_search`, and `om2_enumerate` resolve the people/accounts/deals/channels in your query against the roster server-side and return them in a `resolved_entities` block on the result. Trust those identities over anything a search fuzzily matched, and use them to disambiguate — you do **not** need a separate resolve step.

## Procedure

1. Start with `om2_search` for open questions, or `om2_entity_brief` when the user named a specific account/deal/contact. Read the connected facts, and note the `resolved_entities` the tool anchored on.
2. For a named person/project/doc you just need to locate, use `om2_entity_search`.
3. When completeness matters ("all", "every", "list all"), use `om2_enumerate`, not `om2_search`.
4. For relational or bespoke graph questions the above can't answer, use `om2_graph_schema` then `om2_cypher`.
5. Always be ready to back a claim with `om2_source_trace`.

## If OM2 tools are absent

The network hasn't enabled OM2 (the `enableOM2` flag is off). Don't claim graph results — use `memory_retrieval` and connector search instead.
