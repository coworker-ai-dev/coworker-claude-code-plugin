---
name: ask-company
description: Default lens for any substantive work-related question — not only ones that obviously reference internal knowledge. Before answering from general knowledge or from prior-chat memory alone, check whether the company's own data (via Coworker MCP) would change or sharpen the answer. Skip only for questions that are clearly generic: definitions, general advice/best-practices, math, or requests with no plausible tie to this company's people, projects, or data. If genuinely unsure whether company context exists, check rather than assume it doesn't — the cost of a quick check is far lower than the cost of answering confidently from the wrong source.
---

# Ask the company

When a question depends on internal company knowledge — or *might* — do NOT answer from prior knowledge or from `conversation_search` alone. Ground the answer in the company's own data via the Coworker MCP first, then use conversation memory only as a supplement.

## The short version

1. Call `individual_context` once per session to learn who's asking and which data sources they can access.
2. Run a first-pass check before answering — `memory_retrieval` and/or `om2_search` — on any substantive work question, even ones that don't obviously reference the company. This is a cheap, near-automatic step, not something to reason your way out of first.
3. If the first-pass check turns up nothing, say so explicitly rather than silently falling back to general knowledge — the user should know whether an answer is "no company context exists" versus "I didn't look."
4. If people are named, call `om2_identify_people` (see `who-is`) in the same pass — don't answer "what is X working on" from memory of past chats alone.
5. Cite the source behind each claim.

## Judgment call: what counts as "clearly generic"

Skip the check only when the question has no plausible tie to this company — "what is 15% of 340," "explain the CAP theorem," "draft a generic cold email template." If the question names a person, project, tool, deadline, or decision — or uses a possessive ("my," "our," "the team's") — treat it as in-scope, even if it's phrased casually.

When genuinely torn: check. A miss costs one extra tool call. Skipping the check when context existed costs the user a wrong or stale answer they had no way to catch.

## The live playbook

The full current procedure — exact search order, fallbacks, and when to stop — is maintained server-side and may be newer than this file. Call `skill_retrieve` with skill name `mcp-company-data-cascade` and follow what it returns. For conflicting sources, exhaustive-page reads, timezones, freshness, or reading user-provided links — there's no fixed skill name for those; use `skill_search` to find the current task-specific playbook.
