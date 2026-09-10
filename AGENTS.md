# Agent guidelines

## This repo is PUBLIC

Everything here is visible to anyone on the internet - code, commit messages, PR
titles and descriptions, issues, and comments. It's also the artifact customers
download, so treat every byte as customer-facing.

Never add, in code OR in commit/PR/issue text:

- Credentials, tokens, or API keys (secret-scanning push protection will block
  most of these - don't rely on it as the only check)
- Customer or prospect names, deal details, or usage data
- Internal infrastructure details: hostnames, IPs, database names, environment
  names, ports - anything beyond the public API URLs already in this repo
- Security posture of this or any other repo (branch protection, access lists,
  known weaknesses)
- Employee personal information
- Contents of private repos beyond the file paths already referenced in the
  README

If a change needs internal context to explain it, put that context in the
private core repo's PR or in internal docs, and keep the public commit message
generic. When in doubt, leave it out and ask Bradford.

## Releasing

Skill guidance ships live via `skill_retrieve` rows, and two skills also bundle
a generated copy of their playbook (`skills/*/playbook.md`, `data-quality.md`)
so the model gets the procedure without a separate retrieval call. Regenerate
those copies with `scripts/sync-playbooks.py` whenever the rows change and
bump the version. Shell changes (`hooks/`, the skill roster, `.mcp.json`,
`.claude-plugin/`) also need a version bump and a rebuild in core. See "Releasing" in the README; the
release-reminder workflow opens a `release-needed` issue when this applies.

## Workflow

- All changes to `main` go through a PR (branch protection enforces this).
- Verify locally before merging: `claude --plugin-dir .`
