# Coworker for Claude

Connect Claude — claude.ai, the Cowork desktop app, and Claude Code — to your company's knowledge through the **Coworker MCP**: whatever work tools your company has connected (any subset of 50+ connectors: chat, tickets, code, CRM, docs, email, calendar, support, data warehouses), organizational memory, and the **OM2 knowledge graph** — so Claude answers company questions from your real data instead of guessing.

## What you get

- **One MCP connection** to Coworker (OAuth sign-in in your browser; token cached for future sessions).
- **Skills** that route company questions through Coworker on every surface:
  - `company-data-first` — the mandatory tool order (organizational memory before connector tools), plus what to do when Coworker isn't connected yet
  - `ask-company` — answer internal questions from company data
  - `knowledge-graph` — explore the OM2 graph (people, projects, relationships, themes)
  - `search-memory` — recover past decisions and conventions
  - `who-is` — resolve people to their real identity and org relationships
  - `check-connectors` — see which data sources you can reach
  - `sync-skills` — copy your own local skills into Coworker so they follow you across surfaces
- **Auto-loaded context in Claude Code**: a `SessionStart` hook injects the tool order at session start. (Hooks only run in Claude Code — on other surfaces the same rules arrive via the `company-data-first` skill and the session context the Coworker server attaches to the first tool result.)

## Requirements

- For Claude Code installs: **v2.1.224+** (archive marketplace sources); v2.1.186+ recommended for `claude mcp login`.
- For claude.ai org installs: a Claude **Team or Enterprise** plan with plugins enabled, and an org Owner role to upload.
- A Coworker account whose network has MCP access enabled (`mcpEnabledForNetwork`).

## Install (Claude Code)

```sh
# Add the Coworker marketplace (hosted — no GitHub needed)
/plugin marketplace add https://app.coworker.ai/plugin/marketplace.json

# Install
/plugin install coworker@coworker
```

The plugin points at the Coworker MCP at `https://odin.coworker.ai/mcp`. On first use, a browser opens to sign in with your Google account and authorize access; the token is cached and reused in future sessions.

## What each surface actually delivers

Coworker is one MCP server (`https://odin.coworker.ai/mcp`) reachable from every Claude surface, but the surfaces do NOT deliver the same plugin pieces. This table is the ground truth — plan your rollout around it:

| Surface | Best path | What reaches the model |
|---|---|---|
| **Claude.ai chat** (web + desktop app) | Org Owner uploads this plugin zip (Organization settings → Plugins → Add plugins → Upload a file). claude.ai then shows **Set up connectors for Coworker**: click **Add** (not Skip) and keep the detected defaults (Authentication "Always required"; OAuth client "No client ID, register one automatically"). Set the plugin to Required, set the connector's tools to Always allow (Customize → Connectors), paste Organization instructions. Members click Connect once. Individuals without an org: Customize → Connectors → Add custom connector. | **Tool descriptions**, loaded lazily via tool search, + the **session context** Coworker attaches to the first tool result + Organization instructions + the plugin's **skills** (descriptions always visible; bodies on invocation). MCP server `Instructions` are silently dropped on this surface (anthropics/claude-ai-mcp#93). Hooks and agents never run. **Skip on the connector prompt yields a plugin with no tools**; adding the connector by hand before uploading creates a duplicate. |
| **Claude Cowork** (desktop agent) | Shares the account's claude.ai connectors. Install this plugin via Customize → Plugins (org-published, or add the public repo as a marketplace); Cowork prompts for the connector sign-in. Org admins also flip Organization settings → Cowork → Permissions → Allow "Always allow" for connector tools (off by default). | Skills, hooks, and the plugin's bundled connector; tool descriptions; first-tool-result session context. MCP `Instructions` delivery is not documented. Read-only-annotated tools skip per-call approval. |
| **Claude Code** (CLI/IDE, cloud) | Install this plugin, or `claude mcp add --transport=http coworker https://odin.coworker.ai/mcp`, or org-wide via server-managed settings (`managedMcpServers` + `extraKnownMarketplaces`/`enabledPlugins`). A connector added in claude.ai also appears automatically as `mcp__claude_ai_*`. | Everything: skills, the `SessionStart` hook, MCP `Instructions` **truncated at 2 KB**, tool descriptions **truncated at 2 KB each and deferred behind tool search**, first-tool-result session context. |

All paths use the same OAuth sign-in (Google) and only ever expose tools you have access to.

**The step people miss on claude.ai:** the connector prompt during plugin upload. It has a Skip button, and Skip leaves the org with the skills mounted and no Coworker tools. Click Add and complete the dialog. If a member's chat shows no Coworker tools, they open the chat's tools/connectors menu, enable coworker, and finish the Google sign-in.

### Workspace admins (Team/Enterprise)

- **Upload the plugin and add its connector when asked:** Organization settings → Plugins → Add plugins → Upload a file. On **Set up connectors for Coworker**, click **Add** (never Skip), Continue, and keep the detected defaults (Authentication Always required; OAuth client "No client ID, register one automatically" - Coworker does not support Anthropic's hosted client metadata yet; Managed authorization off; no headers). Set the plugin to **Required**. If a Coworker connector already exists in the org, remove it before uploading or you get a duplicate row.
- **Allow the tools org-wide:** Customize → Connectors → coworker → Tool permissions → **Always allow**, so members don't get an approval prompt on every call. Cowork also needs Organization settings → Cowork → Permissions → Allow "Always allow" for connector tools. Members complete a one-time Google sign-in (Customize → Connectors → Connect).
- **Add Organization instructions** (Organization settings → Organization and access → Organization instructions, 3,000-char cap). On claude.ai chat the MCP server's instructions never reach the model, so this is a real delivery channel, not a backstop. Paste this:

  ```text
  We have Coworker MCP connected as an organization — the source of truth for our
  company's knowledge (people, teams, decisions, policies, projects, customers) and every
  work tool we have connected to it (chat, tickets, code, CRM, docs, email, calendar,
  support, data warehouses, and more; individual_context tells you which) plus the OM2
  knowledge graph.

  When a request depends on internal/company knowledge, use the Coworker tools instead
  of answering from general knowledge:
  - Call individual_context once early to learn who the user is and what data they can access.
  - Search the knowledge graph first (om2_search and the other om2_* tools, when available) before connector-specific search.
  - Use om2_identify_people when people are named.
  Cite the source behind internal claims. If Coworker returns nothing relevant, say so
  rather than guessing.
  ```

## How updates ship (thin-skill architecture)

The zip is deliberately a **stable shell**: skill bodies point at canonical playbooks
maintained server-side as named skills (`mcp-company-data-cascade`,
`mcp-om2-usage`, and whatever `skill_search` turns up for anything else) that Claude
fetches live via `skill_retrieve`. Guidance changes ship by editing those rows - every install
channel (claude.ai zip uploads, hosted marketplace, connectors) picks them up
instantly, with no re-upload and no version bump.

A new zip (and the release steps below) is only needed when the shell itself changes:
hook wiring, the skill roster or their routing descriptions, or `.mcp.json`. When that
happens, claude.ai org admins re-upload the zip; hosted-marketplace installs update via
`/plugin update`.

## How steering works

Plugins can't edit Claude's global system prompt, so Coworker steers behavior through four channels — and because the surfaces differ (see the table above), the channels deliberately overlap:

1. **Skill descriptions** — mounted on every surface that has the plugin, including claude.ai web. `company-data-first` carries the mandatory tool order; the others claim their question shapes.
2. **Tool descriptions + first-tool-result session context** — served by the Coworker MCP itself, so they reach every connected client, plugin or not. The server attaches a short orientation block (who you are, the tool order, playbook names) to the first tool result of each session.
3. **MCP server instructions** — per-network, served at connect time. Delivered in Claude Code and Cowork; claude.ai web currently drops them, which is why channels 1 and 2 exist.
4. **`SessionStart` hook** — Claude Code only (`hooks/session-context.json`); a short pointer at session start: Coworker is the source of truth, follow the server instructions, how to detect the `timezone` argument. It deliberately does not repeat the routing map — the MCP server instructions carry the one canonical copy, and the skill bodies carry it for surfaces that drop server instructions.

> There is no `UserPromptSubmit` hook. There is no separate resolve-first step in the external MCP path — every OM2 tool exposed here carries its own `resolution.entities` in its response envelope, so no `om2_resolve_entities` call or injected representation is needed, and that tool isn't available to call from this surface.

## Layout

```
.claude-plugin/
  plugin.json          # manifest
  marketplace.json     # single-plugin marketplace for internal distribution
.mcp.json              # remote HTTP MCP server (https://odin.coworker.ai/mcp, OAuth 2.1)
hooks/
  hooks.json           # SessionStart (context) + PreToolUse (session tag) hooks — Claude Code only
  session-context.json # additionalContext payload
  client-session.py    # adds client_session_id (this conversation's Claude Code session id) to every Coworker call
skills/
  company-data-first/ ask-company/ knowledge-graph/ search-memory/
  who-is/ check-connectors/ sync-skills/
```

## Notes

- You only ever see/invoke tools whose data sources you have access to — the Coworker MCP enforces per-user connection/OAuth/seat/flag checks server-side.
- The `PreToolUse` hook adds one field, `client_session_id`, to each Coworker tool call: the opaque session UUID Claude Code already assigns the conversation. The Coworker MCP is stateless, so this is how it keeps one activity history per conversation instead of merging a day's calls together. Nothing else is read or sent; if `python3` is missing the hook is a no-op and calls go through unchanged.
- Verify the plugin locally before publishing: `claude --plugin-dir .` then check `/mcp` connects and a "what do we know about…" prompt triggers `individual_context` + `om2_search`.
- Post-deploy MCP smoke test — confirm the plugin reads the shared envelope correctly against the live server:
  - a query that resolves cleanly returns `status: ok` with populated `resolution.entities`
  - a partial match returns `status: partial` and Claude narrows or says what's missing rather than treating it as complete
  - a query with no matches returns `status: no_data` and Claude says so instead of guessing
  - a broad query that returns `retrieval.has_more: true` causes Claude to narrow or page, not present the result as exhaustive
  - an id from one tool result (e.g. an `om2_search` hit) is passed into `om2_source_trace` or `om2_cypher` without ever being shown to the user

## Bundled playbooks are generated. Do not hand-edit them.

`skills/knowledge-graph/playbook.md`, `skills/company-data-first/playbook.md`, and
`skills/company-data-first/data-quality.md` are copies of three server-side skills
(`mcp-om2-usage`, `mcp-company-data-cascade`, `mcp-data-quality`). The server-side
skill is the source of truth; the copies exist so the model gets the procedure without
a separate `skill_retrieve` call. Each file starts with a comment saying so.

Whenever one of those skills changes on the server, someone has to regenerate the copies
here and ship a release. This is a manual step today:

1. Export the three skills as JSON, an array of `{"name": ..., "content": ...}`. From
   Claude Code with the Coworker connector, `skill_retrieve` by name returns the content;
   the Coworker admin tooling can export the same.
2. `scripts/sync-playbooks.py path/to/skills.json` (or `-` for stdin). It rewrites the
   three files and prints what it wrote. It never edits the server.
3. Bump `version` in `.claude-plugin/plugin.json`, commit, PR, then follow the release
   steps below.

Editing `playbook.md` directly gets overwritten on the next sync, and editing the server
skill without syncing leaves the plugin stale. Do both, in that order.

## Releasing (hosted artifacts)

The app serves this plugin as GitHub-free install artifacts — a zip + `marketplace.json`
under `core/frontend-main/public/plugin/`, surfaced on the Coworker MCP settings
page (admin zip upload, `extraKnownMarketplaces` archive install). After merging a plugin
change here:

1. Bump `version` in `.claude-plugin/plugin.json` (drives `/plugin update` detection)
   as part of the change. If a server-side skill changed, regenerate the bundled
   playbooks first (section above).
2. Merge to `main`. The [release-reminder](.github/workflows/release-reminder.yml)
   workflow opens a `release-needed` issue here whenever shell files change - it's
   reminder-only on purpose, so no cross-repo credentials live in this repo.
3. In `core/frontend-main`, run `scripts/build-claude-plugin-zip.sh` (zips this repo's
   `origin/main` and regenerates `marketplace.json` with the new sha256/version), commit
   `public/plugin/*` there, and PR it to `develop`. Close the reminder issue once it ships.
