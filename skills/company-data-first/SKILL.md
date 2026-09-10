---
name: company-data-first
description: MANDATORY routing for any request that touches this company's work - people, teams, customers, deals, projects, decisions, documents, meetings, messages, metrics, what someone is doing, what happened - or anything that lives in Slack, Jira, GitHub, Google Drive, Gmail, Calendar, HubSpot, Salesforce, Zendesk, BigQuery, or Snowflake. Coworker MCP is the source of truth. Call individual_context once, then search organizational memory (om2_* tools) BEFORE any connector, built-in integration, past-chat memory, or general knowledge. Route by question shape: what do we know / what happened with X → om2_search (set time_start for "recent", "yesterday", "this week"); a named account, deal, or contact → om2_entity_brief; a person, including "me"/"my" → om2_identify_people then om2_user_activity (their recent work) or om2_person_network (collaborators); "all / every / list" → om2_enumerate; "what's new", no topic → om2_recent_activity; anything else → om2_graph_schema then om2_cypher. Never switch data sources silently and never answer a company question from prior knowledge. Applies from the first message of a session. If the Coworker tools are missing, this skill says what to do about it.
---

# Company data goes through Coworker first

Coworker MCP is the source of truth for this company's internal knowledge: people, teams, decisions, policies, projects, and customers, via the OM2 knowledge graph and the company's connected tools.

## Mandatory tool order

1. At the start of every new session, call `individual_context` FIRST - who the user is, and which data sources they can reach.
2. For ANY request that requires internal/company knowledge, search the OM2 knowledge graph BEFORE any connector-specific tool, before any non-Coworker integration that covers the same source, and before past-chat memory. Pick the tool by the shape of the question:

   | The user asks about | Call |
   |---|---|
   | what do we know / what happened / what's going on with X | `om2_search`, with `time_start` set for "recent", "yesterday", "this week" |
   | a named account, deal, or contact | `om2_entity_brief` |
   | a person, including "me" / "my" / "I" | `om2_identify_people` (pass `currentUser: true` for the speaker), then `om2_user_activity` for what they have been doing, `om2_person_network` for who they work with |
   | all / every / list all / how many | `om2_enumerate` (`om2_search` is top-K, not exhaustive) |
   | what's new, anything happening - no topic, no person | `om2_recent_activity` |
   | the full history of one thing you already have an id for | `om2_entity_timeline` |
   | something very recent or possibly unindexed | `om2_hybrid_search` |
   | anything the above don't fit | `om2_graph_schema`, then `om2_cypher` |

3. Never call a connector-specific tool until the relevant OM2 lookup has been attempted. The graph spans every source at once; a single connector cannot.
4. When a person is named, resolve them with `om2_identify_people` before acting on the name.
5. When a result is empty or thin: say what you searched, then change the tool or narrow the time window, then check a connector for very recent items. Never switch data sources silently - the user must be able to tell "no company context exists" from "I looked somewhere else".

## Source of truth

- Ground internal claims in Coworker results, not model memory or assumptions.
- If Coworker returns nothing relevant, say so - never guess or fabricate internal information.
- Cite the source behind each internal claim.

## Playbooks

Two are bundled next to this file, regenerated from the server-side rows at each release: `playbook.md` (the company-data search cascade, with worked examples) and `data-quality.md` (conflicting sources, "all" means all, timezones, freshness). Read them when the question is more than a single lookup. The knowledge-graph skill carries the OM2 tool guide. For anything else, or if a bundled copy looks stale, `skill_retrieve` by name (`mcp-company-data-cascade`, `mcp-om2-usage`, `mcp-data-quality`, `mcp-document-retrieval`) returns the live version, and `skill_search` finds task-specific playbooks.

## If the Coworker tools are missing from this session

Do not fail silently, and do not quietly answer from another tool or from memory. Tell the user Coworker isn't reachable in this chat and how to fix it - without asserting a specific cause you can't see:

- **claude.ai / Claude desktop**: open the chat's tools/connectors menu (the "+" or search-and-tools control) and enable the **Coworker** connector. First use prompts a Google sign-in - completing it is what makes the tools appear.
- **Claude Code**: run `/mcp` and check the coworker server's status; `claude mcp add --transport=http coworker https://odin.coworker.ai/mcp` if it's not configured.
- **Workspace admins** manage the Coworker plugin and its connector under the organization's plugin settings.

Once the user has connected, retry the original request through the order above. Falling back to connector search without saying any of this is the one wrong answer.
