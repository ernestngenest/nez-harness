# Codex configuration snapshot

This directory contains the portable Codex configuration exported from the local machine.

## Contents

- `AGENTS.md`: global agent rules and the Anti-Slop Gate.
- `config.toml`: Codex, MCP, project trust, approval, and model settings.
- `docs/`: stack-specific coding rules.
- `rules/`: command execution rules.
- `prompts/`: reusable prompts.
- `hooks.json` and `hooks/`: hook configuration and scripts.
- `skills/`: Codex system skills.
- `agent-skills/`: user-installed skills loaded from `~/.agents/skills`.
- `skill-lock.json`: installed user-skill lock file.
- `plugins/`: installed plugin bundles and metadata.
- `integrations/gbrain/`: reusable GBrain synchronization scripts.

## Secret handling

`CONTEXT7_API_KEY` and the MCP `Authorization` value in `config.toml` are replaced with `REPLACE_ME`. Add valid credentials locally after restoring the configuration.

The snapshot intentionally excludes authentication data, session history, memories, goals, queues, logs, general runtime caches, runtime databases, shell snapshots, lock files, installation identifiers, generated GBrain knowledge, and the 801 MB standalone runtime package. These are machine-specific state rather than portable settings. Installed plugin bundles are retained under `plugins/cache/` because that is Codex's installation location for their skills, agent definitions, assets, and manifests.

## Restore locations

- Copy `AGENTS.md`, `config.toml`, `hooks.json`, `docs/`, `rules/`, `prompts/`, `hooks/`, `skills/`, and `plugins/` into `~/.codex/`.
- Copy `agent-skills/` into `~/.agents/skills/`.
- Copy `skill-lock.json` to `~/.agents/.skill-lock.json`.
- Copy `integrations/gbrain/` into `~/.codex/gbrain-sync/` if the GBrain integration is needed.

Back up existing destination files before restoring this snapshot.
