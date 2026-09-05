---
name: total-review
description: 'Run both fable-review and gpt-review on the current work, then merge their findings, dedupe them, and triage which issues are real vs overthinking. Outputs one clear, concise list of actual issues for the user to approve before fixing. Use when the user says "/total-review", "total review", "review with both", or wants both Fable and GPT reviewers at once. Differentiator: runs BOTH reviewers and triages the merged findings — for a single reviewer use fable-review or gpt-review.'
---

# Total Review

Run both code reviews, merge the findings, and give the user one shortlist of real issues to approve.

## Workflow

1. **Launch both reviewers in parallel** as two bb threads (default). Follow `/nagent`, `/bb-cli`, and each reviewer skill:
   - One `fable-review` worker (Fable 5 Max 1M).
   - One `gpt-review` worker (GPT 5.6 Sol Max).
   - Follow each skill's own instructions exactly: neutral, unbiased prompt; tell it what to review broadly; ask for a detailed report on critical/serious issues; concise plain-English final report.
   - Reuse this thread's environment so both see the same files. Spawn both, then let them work.
   - If the user names another harness (Cursor Task, cmux, Codex CLI, etc.), use that for both instead.

2. **Wait for both to finish** (`bb thread wait` on each, unless another harness was requested). Do not start triage until both reports are back.

3. **Merge and triage.** Read both reports in full. Then:
   - Combine all findings into one list.
   - Dedupe: the same issue reported by both counts once — and is almost certainly real.
   - For each finding, think deeply: is this a real bug / real risk, or is the reviewer overthinking (style preference, theoretical edge case, non-issue)?
   - Be ruthless. Most review findings are overthinking. Only keep issues that genuinely matter.

4. **Output to the user** — clear and very concise:
   - A numbered list of the **actual, real issues** only, each in one line: what it is + where.
   - Mark which reviewer(s) found each: `[both]`, `[fable]`, or `[gpt]`. Issues found by both go first.
   - One short line at the end: how many findings were dropped as overthinking.
   - Then ask the user: approve fixing these, or adjust the list.

5. **On approval, fix and ship.** Fix only the approved issues. Then stage, commit with a clear message, and push to GitHub (per the standard ship workflow). Do not fix anything the user did not approve.

## Rules

- Keep every step's output short and in plain English.
- Do not show the user the raw reviewer reports by default — only the merged shortlist. (The user can ask for the full reports if they want them.)
- Never fix an issue before the user approves the shortlist.
