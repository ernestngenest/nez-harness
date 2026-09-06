---
name: gpt-review-lite
description: 'Launch a GPT 5.6 Medium reviewer as a bb thread (default: /nagent) to do a deep, neutral senior-developer review of the current work and report its findings back verbatim. Cheaper alternative to gpt-review (GPT 5.6 Sol Max). Use when the user says "/gpt-review-lite", "gpt review lite", or asks for a cheaper GPT reviewer. Differentiator: reviewer model is GPT 5.6 Medium — for the max-tier GPT reviewer use gpt-review.'
---

# GPT Review Lite

Launch a GPT 5.6 Medium reviewer to review everything fully and carefully, as if it was a senior developer reviewing the work of a junior. This is the budget alternative to `gpt-review` (which uses GPT 5.6 Sol Max) — same process, cheaper model.

**Default harness is bb.** Read `/nagent` and `/bb-cli` first. Spawn a bb thread with Codex **GPT 5.6** at `medium` reasoning effort (look up the exact model id and reasoning level via the nagent lookup steps — do not guess). Reuse this thread's environment so the reviewer sees the same files. Use `--parent-self` when this thread is coordinating the review. Then `bb thread wait` and show the exact `bb thread output`.

If the user names another harness (Cursor Task, cmux, Codex CLI, etc.), use that instead.

Give it the necessary context, but make sure to stay neutral and unbiased. Do not nudge it towards any one specific solution. The goal here is to do great work. So be as objective and neutral as possible in writing the prompt for the subagent.

Tell him what to review, but don't be overly specific — let him find his own bugs and shortcomings. Just tell him to work extremely hard, to go deep in the review, and to surface any critical or serious issues found in the review.

And when the subagent finishes, show the user his exact response in full. Do not rewrite it. Do not update it.

Again, the goal here is to write great software. It's to build amazing software, and in order to do that you need to let the subagent do its work: tell it what to review in a broad way, be as unbiased as possible, don't influence it in any way, and tell it to output a detailed report — telling us whether the code is good and safe to be merged into production, or whether there are any serious or critical issues with it, and if so, how to fix them.

Also tell him to make the final report concise, written in plain English.
