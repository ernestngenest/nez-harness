# Claude Code config backup

Extracted from `~/.claude` and `~/.claude.json` on this Mac (2026-08-15).

| File/folder | Source | What it is |
|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Global rules (stack conventions, SRP, PR-readiness checklist) |
| `docs/` | `~/.claude/docs/` | Stack-specific rule docs referenced by CLAUDE.md (vue, django, react, nextjs, react-native) |
| `skills/` | `~/.claude/skills/` | Custom/user-authored skills (grilling, tdd, triage, teach, etc.) |
| `commands/` | `~/.claude/commands/` | Custom slash commands |
| `hooks/` | `~/.claude/hooks/` | Shell hooks (e.g. `herdr-agent-state.sh`) |
| `settings.json` | `~/.claude/settings.json` | Hook wiring, statusline, theme, enabled plugins/marketplaces |
| `settings.local.json` | `~/.claude/settings.local.json` | Local permission allowlist |
| `mcp-servers.json` | `mcpServers` key inside `~/.claude.json` | MCP server definitions (context7, browseract) |

## ⚠️ Contains live secrets
`mcp-servers.json` and `settings.local.json` have real API keys/tokens in plain text
(Context7 API key, browser-act bearer token). Don't push this folder to a public
git remote as-is.

## To apply on another PC
Copy/symlink each file back to its source path under `~/.claude/` (create `docs/`,
`skills/`, `commands/`, `hooks/` subfolders as needed), and merge `mcp-servers.json`'s
`mcpServers` object into that machine's `~/.claude.json`.
