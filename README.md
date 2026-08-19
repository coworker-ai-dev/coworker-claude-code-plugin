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
- A Coworker account whose network has MCP access enabled (`mcpEnabledForNetwork`). OM2 tools appear only when your network has `enableOM2` on.

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

Plugins can't edit Claude Code's global system prompt, so this plugin steers behavior four ways, strongest first:

1. **MCP server instructions** — served by the Coworker MCP itself (per-network, includes OM2 guidance when enabled). This reaches every client, not just Claude Code.
2. **`SessionStart` hook** — injects a short instruction to load `individual_context` and prefer Coworker for company knowledge (`hooks/session-context.json`).
3. **`UserPromptSubmit` hook** — auto-runs `om2_resolve_entities` (`type: mcp_tool`) on each prompt, passing the prompt as `text`, and injects the resolved graph node ids alongside it. This mirrors the Coworker chat agent's pre-execution entity resolution, so Claude starts with node ids for the people/accounts/deals/channels the user named instead of having to resolve them mid-task. No-ops on networks without OM2 (the tool isn't present).
4. **Skill descriptions** — Claude invokes the skills above automatically when a request matches.

> The `UserPromptSubmit` hook adds one MCP call per prompt. If that's too costly for a team, remove the `UserPromptSubmit` block from `hooks/hooks.json` and rely on the "resolve first" instruction the MCP already provides.
>
> **Not yet live-tested** — the exact `${prompt}` substitution variable and the `mcp_tool` hook wiring should be smoke-tested in Claude Code before wide rollout.

## Layout

```
.claude-plugin/
  plugin.json          # manifest
  marketplace.json     # single-plugin marketplace for internal distribution
.mcp.json              # remote HTTP MCP server (https://odin.coworker.ai/mcp, OAuth 2.1)
hooks/
  hooks.json           # SessionStart (context) + UserPromptSubmit (auto-resolve entities) hooks
  session-context.json # additionalContext payload
skills/
  ask-company/ knowledge-graph/ search-memory/ who-is/ check-connectors/
```

## Notes

- You only ever see/invoke tools whose data sources you have access to — the Coworker MCP enforces per-user connection/OAuth/seat/flag checks server-side.
- Verify the plugin locally before publishing: `claude --plugin-dir .` then check `/mcp` connects and a "what do we know about…" prompt triggers `individual_context` + `memory_retrieval`/`om2_search`.

## Releasing (hosted artifacts)

The app serves this plugin as GitHub-free install artifacts — a zip + `marketplace.json`
under `core/frontend-main/public/plugin/`, surfaced on the Connect to Claude settings
page (admin zip upload, `extraKnownMarketplaces` archive install). After merging a plugin
change here:

1. Bump `version` in `.claude-plugin/plugin.json` (drives `/plugin update` detection)
   as part of the change.
2. Merge to `main`. The [release-reminder](.github/workflows/release-reminder.yml)
   workflow opens a `release-needed` issue here whenever shell files change - it's
   reminder-only on purpose, so no cross-repo credentials live in this repo.
3. In `core/frontend-main`, run `scripts/build-claude-plugin-zip.sh` (zips this repo's
   `HEAD` and regenerates `marketplace.json` with the new sha256/version), commit
   `public/plugin/*` there, and PR it to `develop`. Close the reminder issue once it ships.
