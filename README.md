# Coworker for Claude Code

Connect Claude Code to your company's knowledge through the **Coworker MCP** — your connected tools (Slack, Jira, GitHub, HubSpot, Salesforce, Google, BigQuery, Snowflake), organizational memory, and the **OM2 knowledge graph** — so Claude answers company questions from your real data instead of guessing.

## What you get

- **One-step connection** to the Coworker MCP (OAuth sign-in in your browser; token cached for future sessions).
- **Auto-loaded context**: a `SessionStart` hook tells Claude to learn who you are and to route company-knowledge questions through Coworker.
- **Skills** that steer Claude toward the right Coworker tools:
  - `ask-company` — answer internal questions from company data
  - `knowledge-graph` — explore the OM2 graph (people, projects, relationships, themes)
  - `search-memory` — recover past decisions and conventions
  - `who-is` — resolve people to their real identity and org relationships
  - `check-connectors` — see which data sources you can reach

## Requirements

- Claude Code **v2.1.224+** (archive marketplace sources) (v2.1.186+ recommended for `claude mcp login`).
- A Coworker account whose network has MCP access enabled (`mcpEnabledForNetwork`).

## Install

```sh
# Add the Coworker marketplace (hosted — no GitHub needed)
/plugin marketplace add https://app.coworker.ai/plugin/marketplace.json

# Install
/plugin install coworker@coworker
```

The plugin points at the Coworker MCP at `https://odin.coworker.ai/mcp`. On first use, Claude Code opens a browser to sign in with your Google account and authorize access; the token is cached and reused in future sessions.

## Connecting from Claude Code, Cowork, or Claude.ai

Coworker is one MCP server (`https://odin.coworker.ai/mcp`) reachable from every Claude surface. Pick your surface:

| Surface | Best path | Steering you get |
|---|---|---|
| **Claude Code** (CLI/IDE) | Install this plugin (below). Or `claude mcp add --transport=http coworker https://odin.coworker.ai/mcp`. | MCP `Instructions` + skills + SessionStart hook |
| **Claude Cowork** (desktop agent) | Install this plugin via Customize → Plugins. Or add the connector: Customize → Plugins → Add connector → Streamable HTTP → the URL → OAuth. | MCP `Instructions` + skills (hook may not fire) |
| **Claude.ai** (web) | Add a custom connector: Settings → Connectors → Add custom connector → the URL → sign in. | MCP `Instructions` only |

All paths use the same OAuth sign-in (Google) and only ever expose tools you have access to.

### Workspace admins (Team/Enterprise)

- **Push it to everyone:** add Coworker as an **organization-managed connector** (or a "required" org plugin for Cowork/Code) so users don't paste URLs. Optionally apply per-tool allow/ask/block policies.
- **Add steering at the workspace level** (recommended — covers users who connect *without* the plugin, since the SessionStart hook only runs in Claude Code): paste this into your workspace/Project system prompt:

  ```text
  This workspace is connected to Coworker — the source of truth for our company's
  knowledge (people, teams, decisions, policies, projects, customers) and connected
  tools (Slack, Jira, GitHub, HubSpot, Salesforce, Google, BigQuery, Snowflake) plus
  the OM2 knowledge graph.

  When a request depends on internal/company knowledge, use the Coworker tools instead
  of answering from general knowledge:
  - Call individual_context once early to learn who the user is and what data they can access.
  - Use memory_retrieval (and om2_search when it's available) before connector-specific search.
  - Use identify_people when people are named.
  Cite the source behind internal claims. If Coworker returns nothing relevant, say so
  rather than guessing.
  ```

  > Note: the MCP server already sends per-network instructions to every client; this workspace prompt is a reliability backstop for clients that under-weight MCP instructions, and for non-plugin connections.

## How updates ship (thin-skill architecture)

The zip is deliberately a **stable shell**: skill bodies point at canonical playbooks
maintained server-side as `public."GlobalSkill"` rows (`mcp-company-data-cascade`,
`mcp-om2-usage`, `mcp-data-quality`, `mcp-document-retrieval`) that Claude fetches live
via `skill_retrieve`. Guidance changes ship by editing those rows - every install
channel (claude.ai zip uploads, hosted marketplace, connectors) picks them up
instantly, with no re-upload and no version bump.

A new zip (and the release steps below) is only needed when the shell itself changes:
hook wiring, the skill roster or their routing descriptions, or `.mcp.json`. When that
happens, claude.ai org admins re-upload the zip; hosted-marketplace installs update via
`/plugin update`.

## How steering works

Plugins can't edit Claude Code's global system prompt, so this plugin steers behavior three ways, strongest first:

1. **MCP server instructions** — served by the Coworker MCP itself (per-network, includes OM2 guidance when enabled). The MCP server supplies the canonical tool descriptions and response-shape guidance; plugin instructions must not duplicate or re-describe how results are represented. This reaches every client, not just Claude Code.
2. **`SessionStart` hook** — injects a short instruction to load `individual_context` and prefer Coworker for company knowledge (`hooks/session-context.json`).
3. **Skill descriptions** — Claude invokes the skills above automatically when a request matches.

> There is no `UserPromptSubmit` hook. There is no separate resolve-first step in the external MCP path — every OM2 tool exposed here carries its own `resolution.entities` in its response envelope, so no `om2_resolve_entities` call or injected representation is needed, and that tool isn't available to call from this surface.

## Layout

```
.claude-plugin/
  plugin.json          # manifest
  marketplace.json     # single-plugin marketplace for internal distribution
.mcp.json              # remote HTTP MCP server (https://odin.coworker.ai/mcp, OAuth 2.1)
hooks/
  hooks.json           # SessionStart (context) hook
  session-context.json # additionalContext payload
skills/
  ask-company/ knowledge-graph/ search-memory/ who-is/ check-connectors/
```

## Notes

- You only ever see/invoke tools whose data sources you have access to — the Coworker MCP enforces per-user connection/OAuth/seat/flag checks server-side.
- Verify the plugin locally before publishing: `claude --plugin-dir .` then check `/mcp` connects and a "what do we know about…" prompt triggers `individual_context` + `memory_retrieval`/`om2_search`.
- Post-deploy MCP smoke test — confirm the plugin reads the shared envelope correctly against the live server:
  - a query that resolves cleanly returns `status: ok` with populated `resolution.entities`
  - a partial match returns `status: partial` and Claude narrows or says what's missing rather than treating it as complete
  - a query with no matches returns `status: no_data` and Claude says so instead of guessing
  - a broad query that returns `retrieval.has_more: true` causes Claude to narrow or page, not present the result as exhaustive
  - an id from one tool result (e.g. an `om2_search` hit) is passed into `om2_source_trace` or `om2_cypher` without ever being shown to the user

## Releasing (hosted artifacts)

The app serves this plugin as GitHub-free install artifacts — a zip + `marketplace.json`
under `core/frontend-main/public/plugin/`, surfaced on the Connect to Claude settings
page (admin zip upload, `extraKnownMarketplaces` archive install). After merging a plugin
change here:

1. Bump `version` in `.claude-plugin/plugin.json` (drives `/plugin update` detection)
   as part of the change.
2. Merge to `main`. The [release-to-core](.github/workflows/release-to-core.yml) workflow
   rebuilds the zip + `marketplace.json` and opens a PR against `villagelabsco/core`
   develop automatically (needs the `CORE_RELEASE_TOKEN` repo secret).
3. Merge that core PR and ship it. Manual fallback: run
   `core/frontend-main/scripts/build-claude-plugin-zip.sh` and commit `public/plugin/*`.
