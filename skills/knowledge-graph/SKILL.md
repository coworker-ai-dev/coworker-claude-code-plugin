---
name: knowledge-graph
description: Explore the company's OM2 organizational knowledge graph — the fastest way to understand people, projects, customers, and how they connect. Use for open-ended "what do we know about X", "how is A related to B", "what's the history of Y", or "what are the themes around Z" questions — and as a first-pass check on narrower work questions where you're not sure if related context exists (a person's current project, a customer's status, what someone did this week, a team's recent activity). Default to a quick check rather than deciding upfront that the question is "too specific" or "already answerable". Route by question shape: what do we know / what happened with X → om2_search (set time_start for "recent", "yesterday", "this week"); a named account, deal, or contact → om2_entity_brief; a person, including "me"/"my" → om2_search with the person's NAME in the query (yours from individual_context; never the literal "I") plus a time window; the exhaustive per-person record → om2_identify_people then om2_user_activity; collaborators → om2_person_network; "all / every / list" → om2_enumerate; "what's new", no topic → om2_recent_activity; anything else → om2_graph_schema then om2_cypher. Answer from the graph; use a connector only for the last few hours, a raw document, or an exact aggregate (JQL, SQL, CRM reports), and name the source. If the om2_* tools aren't in this session, say so and follow company-data-first.
---

# Organizational knowledge graph (OM2)

OM2 is a graph built from the company's connected data. It finds facts that are *indirectly* connected to your query, so it beats single-source search for understanding context. Use it before falling back to per-connector tools when the question is about organizational knowledge — including when you're not certain the question qualifies as "organizational knowledge" until you look.

Refer to OM2 as "organizational memory" and never expose internal node/report IDs to the user.

## Read the playbook

The full usage guide — tool selection, the search→deep-dive workflow, result semantics, completeness signals, anti-loop rules — is in `playbook.md` next to this file. Read it before any non-trivial graph work. It is a copy of the server-side `mcp-om2-usage` skill, regenerated at each release; if you suspect it is stale, `skill_retrieve` with skill name `mcp-om2-usage` returns the live version.

## Quick tool map

Take a name or plain-language query:

`om2_search` — default entry for open questions. Ranked top-K, not exhaustive.
`om2_entity_brief` — the user named a specific account, deal, or contact.
`om2_entity_search` — locate a person, project, or document by name or partial name.
`om2_identify_people` — names or emails (or "me") to exact Person entities. Deterministic roster match, not fuzzy.
`om2_atomic_data` — facts about one concept or entity, without the exhaustive record.
`om2_enumerate` — completeness questions ("all / every / list all").
`om2_hybrid_search` — may not be indexed yet; queries the graph and the live source in parallel.
`om2_user_activity` — what one or more named people (or the current user, `currentUser: true`) have been doing: their facts, newest first, over a date range. This is the tool for "what did I do yesterday", "what has Sam been working on", "catch me up on the platform team".
`om2_recent_activity` — "what's new" across the whole graph with no topic and no person. Network-wide, not per-user.

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

## Time-scoped and first-person questions

"Yesterday", "this week", "since Monday", "recently": always pass `time_start`/`time_end` (macros like `yesterday`, `last monday` work) to `om2_search`, or a date range to `om2_user_activity` / `om2_entity_timeline`. Unscoped search over-retrieves old material. "I", "me", "my": resolve the speaker with `om2_identify_people` (`currentUser: true`) and route to `om2_user_activity`, not to a network-wide tool.

## When a result is empty or thin

Change the tool or narrow the time window, not the source. The graph lags only the last few hours (today's calendar, the latest messages); for those, for a raw document the user asked to read, or for an exact aggregate the source computes (JQL, SQL, CRM reports), use the direct connector tool, and name the source in the answer. Otherwise answer from the graph. It is faster and cheaper than a connector call.

## If OM2 tools are absent

Treat this as an MCP/connector configuration matter — don't assume or state a specific cause you can't see, and never claim graph results. If NO Coworker tools are present at all, tell the user and follow the "If the Coworker tools are missing" steps in the `company-data-first` skill (enable the Coworker connector, complete the sign-in). If other Coworker tools are present but the om2_* family isn't, use Coworker's connector search tools instead and say the graph wasn't available.
