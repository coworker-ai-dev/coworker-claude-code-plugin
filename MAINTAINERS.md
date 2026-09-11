# Maintainer notes

This file is `export-ignore`d: it never ships in the release zip. Everything here is
for people working on the plugin, not for the customers who install it. Customer-facing
documentation lives in `README.md` and nowhere else.

## What ships in the zip

`git archive` of `main` is the zip customers upload to their Claude org. It must contain
only what a plugin needs to run:

```
.claude-plugin/plugin.json
.mcp.json
README.md
hooks/
skills/
```

Everything else (`AGENTS.md`, `CLAUDE.md`, this file, `.github/`, `scripts/`,
`.claude-plugin/marketplace.json`) is listed in `.gitattributes` as `export-ignore`.
When you add a new file that isn't one of the five above, add it there too. Two checks
enforce this: the `archive-check` workflow on every PR, and
`core/frontend-main/scripts/build-claude-plugin-zip.sh`, which refuses to build a zip
containing anything else.

## claude.ai plugin validation

claude.ai validates the zip on upload and rejects the whole plugin if any `SKILL.md`
`description` exceeds **1024 characters**. (This is stricter than Claude Code, which
only truncates.) `archive-check` fails PRs over the limit; the build script does too.
Keep descriptions short and put the procedure in the skill body.

## How updates ship (thin-skill architecture)

The zip is deliberately a **stable shell**: skill bodies point at canonical playbooks
maintained server-side as named skills (`mcp-company-data-cascade`, `mcp-om2-usage`,
and whatever `skill_search` turns up for anything else) that Claude fetches live via
`skill_retrieve`. Guidance changes ship by editing those rows; every install channel
(claude.ai zip uploads, hosted marketplace, connectors) picks them up instantly, with
no re-upload and no version bump.

A new zip (and the release steps below) is only needed when the shell itself changes:
hook wiring, the skill roster or their routing descriptions, `.mcp.json`, or the bundled
playbooks. When that happens, claude.ai org admins re-upload the zip; hosted-marketplace
installs update via `/plugin update`.

## How steering works

Plugins can't edit Claude's global system prompt, so Coworker steers behavior through four
channels. Because the surfaces differ, the channels deliberately overlap:

1. **Skill descriptions**: mounted on every surface that has the plugin, including
   claude.ai web. `company-data-first` carries the mandatory tool order; the others claim
   their question shapes.
2. **Tool descriptions + first-tool-result session context**: served by the Coworker MCP
   itself, so they reach every connected client, plugin or not. The server attaches a
   short orientation block (who you are, the tool order, playbook names) to the first
   tool result of each session.
3. **MCP server instructions**: per-network, served at connect time. Delivered in Claude
   Code and Cowork; claude.ai web currently drops them (anthropics/claude-ai-mcp#93),
   which is why channels 1 and 2 exist. Claude Code truncates them at 2 KB, and tool
   descriptions at 2 KB each behind tool search.
4. **`SessionStart` hook**: Claude Code only (`hooks/session-context.json`); a short
   pointer at session start: Coworker is the source of truth, follow the server
   instructions, how to detect the `timezone` argument. It deliberately does not repeat
   the routing map; the MCP server instructions carry the one canonical copy, and the
   skill bodies carry it for surfaces that drop server instructions.

There is no `UserPromptSubmit` hook. There is no separate resolve-first step in the
external MCP path: every OM2 tool exposed here carries its own `resolution.entities` in
its response envelope, so no `om2_resolve_entities` call is needed and that tool isn't
available from this surface.

## Layout

```
.claude-plugin/
  plugin.json          # manifest (ships)
  marketplace.json     # single-plugin marketplace for `/plugin marketplace add <repo>` (repo only)
.mcp.json              # remote HTTP MCP server (https://odin.coworker.ai/mcp, OAuth 2.1)
hooks/
  hooks.json           # SessionStart (context) + PreToolUse (session tag) hooks — Claude Code only
  session-context.json # additionalContext payload
  client-session.py    # adds client_session_id (the Claude Code session id) to every Coworker call
skills/
  company-data-first/ ask-company/ knowledge-graph/ search-memory/
  who-is/ check-connectors/ sync-skills/
scripts/
  sync-playbooks.py    # regenerates the bundled playbooks (repo only)
```

## Bundled playbooks are generated. Do not hand-edit them.

`skills/knowledge-graph/playbook.md`, `skills/company-data-first/playbook.md`, and
`skills/company-data-first/data-quality.md` are copies of three server-side skills
(`mcp-om2-usage`, `mcp-company-data-cascade`, `mcp-data-quality`). The server-side
skill is the source of truth; the copies exist so the model gets the procedure without
a separate `skill_retrieve` call. Each file starts with a comment saying so.

Whenever one of those skills changes on the server, regenerate the copies and ship a
release:

1. Export the three skills as JSON, an array of `{"name": ..., "content": ...}`. From
   Claude Code with the Coworker connector, `skill_retrieve` by name returns the content;
   the Coworker admin tooling can export the same.
2. `scripts/sync-playbooks.py path/to/skills.json` (or `-` for stdin). It rewrites the
   three files and prints what it wrote. It never edits the server.
3. Bump `version` in `.claude-plugin/plugin.json`, commit, PR, then follow the release
   steps below.

Editing `playbook.md` directly gets overwritten on the next sync, and editing the server
skill without syncing leaves the plugin stale. Do both, in that order.

## Verifying locally

- `claude --plugin-dir .` then check `/mcp` connects and a "what do we know about…"
  prompt triggers `individual_context` + `om2_search`.
- Build the zip the way core does and upload it to a claude.ai org **before** merging any
  release: `git archive --format=zip HEAD -o /tmp/coworker-plugin.zip`, then Organization
  settings → Plugins → Add plugins → Upload a file. A validation error there is a
  release blocker.
- Post-deploy MCP smoke test against the live server:
  - a query that resolves cleanly returns `status: ok` with populated `resolution.entities`
  - a partial match returns `status: partial` and Claude narrows or says what's missing
  - a query with no matches returns `status: no_data` and Claude says so instead of guessing
  - a broad query returning `retrieval.has_more: true` makes Claude narrow or page
  - an id from one tool result is passed into `om2_source_trace` or `om2_cypher` without
    ever being shown to the user

## Releasing (hosted artifacts)

The app serves this plugin as GitHub-free install artifacts: a zip + `marketplace.json`
under `core/frontend-main/public/plugin/`, surfaced on the Coworker MCP settings page
(admin zip upload, `extraKnownMarketplaces` archive install). After merging a plugin
change here:

1. Bump `version` in `.claude-plugin/plugin.json` (drives `/plugin update` detection)
   as part of the change. If a server-side skill changed, regenerate the bundled
   playbooks first (section above).
2. Merge to `main`. The [release-reminder](.github/workflows/release-reminder.yml)
   workflow opens a `release-needed` issue here whenever shell files change; it's
   reminder-only on purpose, so no cross-repo credentials live in this repo.
3. In `core/frontend-main`, run `scripts/build-claude-plugin-zip.sh` (zips this repo's
   `origin/main`, verifies the contents, and regenerates `marketplace.json` with the new
   sha256/version), commit `public/plugin/*` there, and PR it to `develop`. Close the
   reminder issue once it ships.
