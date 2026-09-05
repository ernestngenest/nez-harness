# OpenCode profile

Adapted from `claude-code/` to OpenCode's native config conventions.

| File/folder | OpenCode source | What it is |
|---|---|---|
| `AGENTS.md` | `~/.config/opencode/AGENTS.md` | Global rules — same content as `claude-code/CLAUDE.md`, paths in the stack-doc table updated to the OpenCode docs location |
| `docs/` | `~/.config/opencode/docs/` | Stack-specific rule docs referenced by `AGENTS.md` (vue, django, react, nextjs, react-native) — unchanged copies |
| `skills/` | `~/.config/opencode/skills/` | Same `SKILL.md` folders as `claude-code/skills/` — OpenCode's skill format is directly compatible (`<name>/SKILL.md`) |
| `command/` | `~/.config/opencode/command/` | Custom slash commands, converted from Claude Code's `commands/*.md` frontmatter (`description`) to OpenCode's (`description`, `agent`) |
| `opencode.jsonc` | `~/.config/opencode/opencode.jsonc` | MCP server definitions (context7, browseract), ported from `claude-code/mcp-servers.json` using OpenCode's `{env:VAR}` interpolation instead of hardcoded secrets |

## Not ported

- `settings.json` (plugins/marketplaces, hook wiring, statusline, theme) — Claude Code-specific concepts with no OpenCode equivalent.
- `hooks/herdr-agent-state.sh` — managed by the herdr integration installer, not hand-copied config. Install herdr's own OpenCode integration on a machine that needs it.
- `settings.local.json` — Claude Code's local permission allowlist; OpenCode has its own permission config (`permission` key in `opencode.jsonc`) if needed later.

## To apply on another PC

```
mkdir -p ~/.config/opencode
cp opencode/AGENTS.md ~/.config/opencode/AGENTS.md
cp -R opencode/docs ~/.config/opencode/docs
cp -R opencode/skills ~/.config/opencode/skills
cp -R opencode/command ~/.config/opencode/command
cp opencode/opencode.jsonc ~/.config/opencode/opencode.jsonc
```

Set `CONTEXT7_API_KEY` and `BROWSERACT_TOKEN` in the shell environment OpenCode runs in — `opencode.jsonc` reads them via `{env:VAR}` instead of storing them in the file.
