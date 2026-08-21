---
name: who-is
description: Resolve people mentioned by name or email to their real identity within the company — role, team, manager, peers, and direct reports. Use whenever the user names a person ("ask Sarah", "who owns X", "loop in the platform team") and you need to know who they actually are. Calls the Coworker MCP om2_identify_people tool.
---

# Who is this person

Use the Coworker MCP `om2_identify_people` tool to map names/emails to real identities.

## Procedure

1. Call `om2_identify_people` with `names` and/or `emails` as JSON arrays (e.g. `{"names": ["Sarah", "Dan"]}`).
2. Set `currentUser: true` to identify the person you're talking to.
3. Use `om2_person_network` on a returned node_id for a person's CLOSE_TO collaborators.

## Notes

- Returns identified users (name, email, role) plus an `unknown_users` list for names that didn't match — surface unresolved names rather than guessing.
- Use the resolved email/role downstream (e.g. to scope a Slack or Jira search to the right person).
