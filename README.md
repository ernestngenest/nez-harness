# Nez Harness

Portable coding-agent configuration for three providers: **Claude Code**, **Codex**, and **OpenCode**. Each profile is a self-contained snapshot of the global rules, skills, commands, and MCP server config used on this machine, so the same setup can be restored on another machine or read into `bb`.

## Structure

| Profile | Directory | Native destination |
|---|---|---|
| Claude Code | `claude-code/` | `~/.claude/` |
| Codex | `codex/` | `~/.codex/` |
| OpenCode | `opencode/` | `~/.config/opencode/` |

Each directory has its own `README.md` with the exact file-by-file breakdown and secret-handling notes for that provider. Skills are authored once (mostly under `claude-code/skills/`) and mirrored into `codex/agent-skills/` and `opencode/skills/` — all three use a compatible `<skill-name>/SKILL.md` folder format.

## Install

Pick the profile(s) you need and copy them into place:

```bash
# Claude Code
cp claude-code/CLAUDE.md ~/.claude/CLAUDE.md
cp -R claude-code/skills ~/.claude/skills
cp -R claude-code/commands ~/.claude/commands
cp -R claude-code/hooks ~/.claude/hooks
cp claude-code/settings.json ~/.claude/settings.json
# claude-code/mcp-servers.json and settings.local.json contain live secrets and
# are gitignored — merge those by hand, see claude-code/README.md

# Codex
cp codex/AGENTS.md codex/config.toml codex/hooks.json ~/.codex/
cp -R codex/docs codex/rules codex/prompts codex/hooks codex/skills ~/.codex/
cp -R codex/agent-skills ~/.agents/skills
# config.toml ships with CONTEXT7_API_KEY/Authorization as REPLACE_ME — fill
# in real values locally, see codex/README.md

# OpenCode
mkdir -p ~/.config/opencode
cp opencode/AGENTS.md ~/.config/opencode/AGENTS.md
cp -R opencode/docs ~/.config/opencode/docs
cp -R opencode/skills ~/.config/opencode/skills
cp -R opencode/command ~/.config/opencode/command
cp opencode/opencode.jsonc ~/.config/opencode/opencode.jsonc
# opencode.jsonc reads secrets via {env:VAR} — export CONTEXT7_API_KEY and
# BROWSERACT_TOKEN in the shell OpenCode runs in, see opencode/README.md
```

Back up existing destination files first — none of these commands merge, they overwrite.

## Secrets

No profile commits real credentials:

- `claude-code/mcp-servers.json` and `claude-code/settings.local.json` are gitignored entirely.
- `codex/config.toml` ships with `CONTEXT7_API_KEY` and the MCP `Authorization` header redacted to `REPLACE_ME`.
- `opencode/opencode.jsonc` uses `{env:VAR}` interpolation instead of storing values at all.

All three profiles ship a `secrets` skill (`bb secret request ...`) so an agent can request credentials from the user through `bb` rather than asking them to paste values into chat.

## Not currently used

- `pi/`, `scripts/`, `package.json`, `package-lock.json`, `node_modules/` — leftovers from an earlier attempt to run this profile through the Pi coding-agent runtime. That approach was abandoned in favor of each provider's own native config, and these are gitignored/untracked; safe to delete.
