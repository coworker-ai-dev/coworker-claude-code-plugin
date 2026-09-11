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

## Bundled playbooks

`skills/knowledge-graph/playbook.md`, `skills/company-data-first/playbook.md`, and
`skills/company-data-first/data-quality.md` are GENERATED from three server-side
skills (`mcp-om2-usage`, `mcp-company-data-cascade`, `mcp-data-quality`). Never
edit them by hand. When a server-side skill changes, export the three skills as
JSON and run `scripts/sync-playbooks.py <file>`; then bump the version and
release. If you are changing the guidance itself, change the server-side skill
first, then sync. Full recipe: "Bundled playbooks are generated" in MAINTAINERS.md.

## Releasing

Most skill guidance ships live via `skill_retrieve`; only the three bundled
playbooks above need a sync. Shell changes (`hooks/`, the skill roster,
`.mcp.json`, `.claude-plugin/`, the bundled playbooks) need a version bump and
a rebuild in core. See "Releasing" in MAINTAINERS.md; the release-reminder workflow
opens a `release-needed` issue when this applies.

## The release zip

`git archive` of this repo IS the customer download. Only runtime files ship:
`.claude-plugin/plugin.json`, `.mcp.json`, `README.md`, `hooks/`, `skills/`.
Anything else you add must go in `.gitattributes` as `export-ignore`, and
`README.md` must stay customer-facing only (maintainer docs go in
`MAINTAINERS.md`). claude.ai rejects the whole plugin if any `SKILL.md`
`description` is over 1024 characters. The `archive-check` workflow and core's
build script both enforce these.

## Workflow

- All changes to `main` go through a PR (branch protection enforces this).
- Verify locally before merging: `claude --plugin-dir .`
