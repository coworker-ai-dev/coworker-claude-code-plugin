# Coworker for Claude

Connect Claude — claude.ai, the Cowork desktop app, and Claude Code — to your company's knowledge through the **Coworker MCP**: the work tools your company has connected (chat, tickets, code, CRM, docs, email, calendar, support, data warehouses), organizational memory, and the **OM2 knowledge graph** — so Claude answers company questions from your real data instead of guessing.

## What you get

- **One MCP connection** to Coworker (OAuth sign-in in your browser; token cached for future sessions).
- **Skills** that route company questions through Coworker on every surface:
  - `company-data-first` — the tool order (organizational memory before connector tools), plus what to do when Coworker isn't connected yet
  - `ask-company` — answer internal questions from company data
  - `knowledge-graph` — explore the OM2 graph (people, projects, relationships, themes)
  - `search-memory` — recover past decisions and conventions
  - `who-is` — resolve people to their real identity and org relationships
  - `check-connectors` — see which data sources you can reach
  - `sync-skills` — copy your own local skills into Coworker so they follow you across surfaces
- **Auto-loaded context in Claude Code**: a `SessionStart` hook points Claude at Coworker at session start. (Hooks only run in Claude Code; on other surfaces the same guidance arrives via the skills and the Coworker server itself.)

You only ever see and invoke tools whose data sources you have access to. Access is enforced by the Coworker server, per user.

## Requirements

- For claude.ai org installs: a Claude **Team or Enterprise** plan with plugins enabled, and an org Owner role to upload.
- For Claude Code installs: **v2.1.224+**.
- A Coworker account with MCP access enabled for your workspace.

## Install on claude.ai (Team / Enterprise admins)

One upload covers everyone on web and desktop.

1. **Upload the plugin:** Organization settings → Plugins → Add plugins → Upload a file, and pick this zip.
2. **Add the connector when asked.** claude.ai shows **Set up connectors for Coworker**. Click **Add** (not Skip), Continue, and keep the detected defaults (Authentication "Always required"; OAuth client "No client ID, register one automatically"; Managed authorization off; no headers). Skip leaves the org with the skills mounted and no Coworker tools. If a Coworker connector already exists in the org, remove it before uploading or you get a duplicate.
3. **Set the plugin to Required.**
4. **Allow the tools org-wide:** Customize → Connectors → coworker → Tool permissions → **Always allow**, so members don't get an approval prompt on every call. For Cowork, also set Organization settings → Cowork → Permissions → Allow "Always allow" for connector tools.
5. **Add Organization instructions** (Organization settings → Organization and access → Organization instructions). Paste this:

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

Members then complete a one-time sign-in: Customize → Connectors → coworker → Connect. If a member's chat shows no Coworker tools, they open the chat's tools/connectors menu, enable coworker, and finish the sign-in.

Individuals without an org: Customize → Connectors → Add custom connector, URL `https://odin.coworker.ai/mcp`.

## Install in Claude Code

```sh
# Add the Coworker marketplace (hosted — no GitHub needed)
/plugin marketplace add https://app.coworker.ai/plugin/marketplace.json

# Install
/plugin install coworker@coworker
```

Or, without the plugin: `claude mcp add --transport=http coworker https://odin.coworker.ai/mcp`. Org-wide rollout works through server-managed settings (`managedMcpServers`, `extraKnownMarketplaces`, `enabledPlugins`). A connector added in claude.ai also appears automatically in Claude Code.

On first use, a browser opens to sign in and authorize access; the token is cached and reused in future sessions.

## Install in Claude Cowork

Cowork shares your claude.ai connectors. Install the plugin via Customize → Plugins (org-published, or from the marketplace above); Cowork prompts for the connector sign-in.

## Privacy notes

- The Coworker MCP only exposes tools for data sources you personally have access to.
- In Claude Code, a `PreToolUse` hook adds one field, `client_session_id`, to each Coworker tool call: the opaque session UUID Claude Code already assigns the conversation. This lets Coworker keep one activity history per conversation. Nothing else is read or sent; if `python3` is missing the hook is a no-op and calls go through unchanged.

## Support

Questions or problems: reach your Coworker contact, or see https://coworker.ai.
