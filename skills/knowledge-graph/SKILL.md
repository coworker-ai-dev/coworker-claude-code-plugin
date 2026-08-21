---
name: knowledge-graph
description: Explore the company's OM2 organizational knowledge graph — the fastest way to understand people, projects, customers, and how they connect. Use for open-ended "what do we know about X", "how is A related to B", "what's the history of Y", or "what are the themes around Z" questions. Only applies when OM2 tools (om2_*) are available in this session; if they aren't, fall back to connector search.
---

# Organizational knowledge graph (OM2)

OM2 is a graph built from the company's connected data. It finds facts that are *indirectly* connected to your query, so it beats single-source search for understanding context. Use it before falling back to per-connector tools when the question is about organizational knowledge.

Refer to OM2 as "organizational memory" and never expose internal node/report IDs to the user.

## Get the live guide first

The full, current usage guide — tool selection, procedure, result semantics, completeness/pagination signals, cypher recipes, anti-loop rules — is maintained server-side and may be newer than this file. Before any non-trivial graph work, call `skill_retrieve` with skill name `om2-memory-usage` and follow what it returns.

## Quick tool map

Take a name or plain-language query:

`om2_search` — default entry for open questions. Ranked top-K, not exhaustive.
`om2_entity_brief` — the user named a specific account, deal, or contact.
`om2_entity_search` — locate a person, project, or document by name or partial name.
`om2_identify_people` — names or emails (or "me") to exact Person entities. Deterministic roster match, not fuzzy.
`om2_atomic_data` — facts about one concept or entity, without the exhaustive record.
`om2_enumerate` — completeness questions ("all / every / list all").
`om2_hybrid_search` — may not be indexed yet; queries the graph and the live source in parallel.
`om2_recent_activity` — "what's new" with no specific query.

Take an ID from a prior result, not a name:

`om2_node_details` — everything about one node: properties, connections, recent mentions, close-to people.
`om2_entity_timeline` — the complete record for one entity, where search would silently truncate.
`om2_person_network` — a person's close collaborators and shared work context.
`om2_document_explore` — facts referencing a document, plus its editors and owners.
`om2_source_trace` — recover the source behind a fact, to cite or verify (needs an su_id).
`om2_report_explore` — read one report in full: every fact, mentioned entities, source documents.

Power path:

`om2_graph_schema` + `om2_cypher` — bespoke graph-shaped questions the tools above don't cover. Cypher explores from known entry points; it won't find them for you.

Not every tool takes a plain-language query — the six ID tools and `om2_cypher` need an ID from a prior tool's result. The normal shape of an investigation is an entry tool to find the node, then an ID tool to go deep.

## If OM2 tools are absent

Treat this as an MCP/connector configuration matter, not a flag you can reason about — don't assume or state a specific cause. Don't claim graph results — use connector search instead.
