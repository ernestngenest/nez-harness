---
name: reset-cursor-acp
description: 'Reset a stuck, hung, frozen, or buggy Cursor ACP agent inside bb, and reload its Cursor config (rules, skills, mcp.json). Use when the user says "reset cursor acp", "cursor is stuck in bb", "cursor thread hangs", "restart the cursor agent", "reload cursor config in bb", or a bb thread on the Cursor provider stops responding. Differentiator: bb-only, Cursor-only, one script. For resuming cursor-agent terminal sessions use cursor-cli; for general bb thread control use bb-cli.'
---

# Reset Cursor ACP in bb

## How Cursor ACP works in bb (read this first)

- ACP = Agent Client Protocol, an open standard from Zed. bb is the client, Cursor CLI is the server.
- bb's `provider-acp` plugin spawns one `cursor-agent acp` subprocess **per thread, on demand**, owned by a `bb-provider-bridge-worker` process. They talk JSON-RPC over stdin/stdout.
- **There is no global Cursor ACP server.** Nothing to keep alive with launchd or a watchdog. Never build one.
- Config (rules, skills, `.cursor/mcp.json`) is read when the subprocess starts. Reload = spawn a new subprocess.
- `bb thread stop <id>` releases the runtime and kills the subprocess. The thread history is kept. The next message spawns a fresh `cursor-agent acp`.

## Quick reset

Resolve `scripts/reset-cursor-acp.sh` relative to this `SKILL.md`. Run:

```bash
scripts/reset-cursor-acp.sh <thread-id>      # reset one Cursor thread
scripts/reset-cursor-acp.sh --self           # reset the current thread (BB_THREAD_ID)
scripts/reset-cursor-acp.sh                  # no thread: orphan cleanup + health check only
scripts/reset-cursor-acp.sh --dry-run        # show what would happen
scripts/reset-cursor-acp.sh <id> --kill-all  # also kill live agents of OTHER Cursor threads
```

Find Cursor thread ids with `bb status` (current thread) or:

```bash
bb thread list --json | python3 -c 'import json,sys; [print(t["id"], t["status"], t["title"]) for t in json.load(sys.stdin) if t.get("providerId")=="acp-cursor"]'
```

The script does four things in order:

1. `bb thread stop <id>` to release the runtime.
2. Kills orphaned `cursor-agent acp` processes (parent is gone or not a bb bridge worker). Live agents of other threads are kept unless `--kill-all`.
3. Prints Cursor CLI version, login state, and whether `bb updates status` shows a newer Cursor CLI.
4. Tells you to send the next message.

If `ps` fails with "operation not permitted", the agent shell is sandboxed. Re-run the script outside the sandbox.

## Verify

After the script: send one short message to the thread. A fresh agent answers within seconds. If it hangs again, work through the causes below before resetting a second time.

## Known causes (check before blind resets)

- **Old Cursor CLI.** Most ACP bugs get fixed in CLI releases. If step 3 shows an update, run `bb updates apply`, then reset again.
- **Expired login.** Symptom "Failed to initialize session services". Fix: `cursor-agent login`, then reset.
- **Unanswered permission request.** Cursor blocks until the client answers `session/request_permission`. Cursor's built-in web search tool always prompts, even in unrestricted mode. Check the thread for a pending approval and answer it before resetting.
- **Session resume failed.** Cursor's `session/load` often returns "Session not found". A fresh session after `bb thread stop` is the fix, not a retry.
- **Team-level MCP servers** from the Cursor dashboard do not work in ACP mode. Only project or user `.cursor/mcp.json`.
- **Rate limits.** Enable bb's `provider-retry` plugin (`bb plugin enable provider-retry`) so rate-limit failures retry instead of failing the turn.

## Do not

- Do not add launchd KeepAlive, cron, or any watchdog for `cursor-agent acp`. There is no long-lived process to watch.
- Do not `pkill -f cursor-agent` blindly. That kills every Cursor thread in bb and the interactive TUI. Use the script; it only kills orphans by default.
- Do not restart the whole bb app for a single stuck thread. `bb thread stop` is enough.
- Do not use `bb thread compact` on Cursor threads. Cursor does not support it.
