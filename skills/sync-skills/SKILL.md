---
name: sync-skills
description: Sync, transfer, or export the user's Claude Code / Cowork skills into Coworker so they're available across surfaces. Use only when the user explicitly asks to sync/transfer/export their skills to Coworker. Reads the available-skills list from this session and creates the user-authored ones as Coworker skills.
---

# Sync skills to Coworker

When the user asks to sync, transfer, or export their skills to Coworker, follow these steps.

1. **Read the available skills list** from the system-reminder in this conversation — the block that lists available skills with their descriptions.

2. **Filter out default/built-in skills** (they ship with Claude Code and aren't user-authored): update-config, keybindings-help, verify, code-review, fewer-permission-prompts, loop, schedule, claude-api, run, init, review, security-review.

3. **Filter out plugin skills** — any skill with a colon in its name (e.g. `caveman:caveman`, `chrome-devtools-mcp:chrome-devtools`). These come from installed plugins, not the user.

4. **For each remaining skill**, call `skill_create` with:
   - `skill_id`: the skill name as listed
   - `title`: the skill name, title-cased
   - `content`: the description from the skills list
   - `short_description`: the description from the skills list

5. **Report** a short table of what was synced and what was skipped (and why).

You can proactively offer this when the user first connects: "I noticed you have custom skills — want me to sync them to Coworker so they're available across your tools?"
