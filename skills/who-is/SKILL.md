---
name: who-is
description: Resolve people mentioned by name, email, role, or team reference to their real identity within the company — role, team, manager, peers, and direct reports. Use whenever the user names or clearly refers to a person or team ('ask Sarah', 'who owns X', 'loop in the platform team', 'what is Tom working on') — not only when the ask is explicitly about identity. A question that merely *contains* a name (e.g. 'what's Tom working on') still needs this — don't substitute conversation_search or past-chat recall for resolving who the person actually is and pulling their current state from live sources. Calls the Coworker MCP `om2_identify_people` tool.
---

# Who is this person

Use the Coworker MCP `om2_identify_people` tool to map names/emails to real identities.

## Procedure

1. Call `om2_identify_people` with `names` and/or `emails` as JSON arrays (e.g. `{"names": ["Sarah", "Dan"]}`).
2. Set `currentUser: true` to identify the person you're talking to.
3. Use `om2_person_network` on a returned node_id for a person's CLOSE_TO collaborators.
4. If the question is about what that person is *currently* doing (not just who they are), don't stop at identity resolution — follow up with a live connector or knowledge-graph query (see `ask-company` / `knowledge-graph`) scoped to their resolved identity. Answering "what is X working on" from a summary of a past chat, without this step, is treating stale conversation memory as if it were current company state — avoid that.

## Notes

- Returns identified users (name, email, role) plus an `unknown_users` list for names that didn't match — surface unresolved names rather than guessing.
- Use the resolved email/role downstream (e.g. to scope a Slack or Jira search to the right person).
