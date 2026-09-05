---
name: secrets
description: Securely request API keys, access tokens, passwords, webhook secrets, or other credentials and write them to a dotenv file without exposing their values to the agent. Use whenever a task needs a credential that the user must supply.
---

# Request secrets securely

Never ask the user to paste a secret value into chat, and never read, print, or log a completed secret-bearing file to "verify" it. The core rule is the same everywhere this skill runs: the credential value must never pass through the agent's own context — only the destination path and success/failure state may.

Batch every currently known variable into one request. Inspect documentation or `.env.example` to identify variable names, but do not read or print an existing secret-bearing env file.

## When `bb` is available

If the `bb` CLI is on PATH (or `BB_THREAD_ID` is set in the environment), use `bb secret request` — it prompts the user out-of-band and writes the result directly to a dotenv file:

```bash
bb secret request OPENAI_API_KEY RESEND_API_KEY \
  --purpose "Configure application credentials" \
  --describe OPENAI_API_KEY "OpenAI API key used by the server" \
  --describe RESEND_API_KEY "Resend API key used for transactional email" \
  --write-env .env.local
```

Always provide the exact `--write-env` destination, a concise purpose, and one short plain-language description per variable. Relative destinations resolve from the CLI working directory; absolute destinations may point anywhere on the thread's host. Never place secret values in argv, prompts, comments, logs, or follow-up messages.

After success, trust the command's path and added/updated/unchanged counts. Never verify by running `cat`, `sed`, `env`, or another command that would reveal the completed file.

If the command reports duplicate dotenv assignments, fix the file structure without reading values and rerun the request. If it reports repeated write conflicts, rerun the same request; do not ask the user to paste values. Under the workspace sandbox (Accept Edits / Approve for me), Claude's macOS sandbox permits the loopback access plugin CLI commands need; Linux and other provider sandboxes may still require escalation approval.

## When `bb` is not available

Running standalone (no `bb`, no equivalent secret-broker tool on this host), there is no way for the agent to collect a secret without it passing through the conversation. In that case, don't collect it at all:

1. State the exact target file path and the variable name(s) needed, with a one-line description of what each is for.
2. Ask the user to add the lines directly to that file themselves (in their own editor, outside the chat).
3. Wait for them to confirm it's done, then proceed — do not open, read, or `cat` the file afterward to check.

If the destination file doesn't exist yet, it's fine to create it with placeholder lines (`VAR_NAME=`) so the user only has to fill in the value, as long as no real value is ever written by the agent itself.
