---
name: ras-mic-workflow
description: End-to-end feature-delivery flow from Micky/@Rasmic's "Software Factory" — isolated worktree, then code-structure discipline, then evidence-driven testing, before/after screenshots, and iterating with Greptile until the PR is clean. Use when the user says "ras mic workflow", "rasmic workflow", "software factory flow", or wants to ship a feature start-to-finish using new-feature + code-structure + evidence-driven-testing + before-and-after + greploop/greploop-apps together instead of one at a time.
---

# Ras Mic Workflow

Source: [Micky (@Rasmic)](https://x.com/Rasmic), "a 'software factory' is more about your workflows + skills + domain knowledge than it is some harness" (Aug 20, 2026). This skill chains five already-installed skills into one ordered flow instead of invoking them separately.

Harness-agnostic and model-agnostic: every step below is itself a skill, so this works the same in Claude Code, Codex, OpenCode, or bb.

## Prerequisites

The repo has an `AGENTS.md` / `CLAUDE.md` with project context and conventions. If it doesn't, write one first — every step below leans on it for domain knowledge.

## Steps

1. **`new-feature`** — start the task in an isolated Git worktree branched from `origin/main`. Never write code directly on a shared branch.
2. **`code-structure`** — while implementing, decide what belongs in actions vs shared services. If this feature duplicates logic another workflow already has, extract it instead of copy-pasting.
3. **`evidence-driven-testing`** — test the feature hands-on (computer use or scripted probes) while recording proof: screen recording with test/assertion annotations, or measured before/after numbers for non-UI changes.
4. **`before-and-after`** — for UI changes, capture before/after screenshots of the affected pages or elements to attach to the PR.
5. **`greploop`** (or **`greploop-apps`** for large PRs that exceed Greptile's file-count limit) — open the PR, trigger Greptile review, fix every actionable comment, push, and repeat until Greptile reports 5/5 confidence with zero unresolved comments.

## When to stop early

- Prototyping or throwaway spikes: skip straight to `new-feature` only, or use the `prototype` skill instead — this flow is for work headed to a real PR.
- No UI touched: skip `before-and-after`, keep `evidence-driven-testing` (it also covers headless/measured evidence).
- No Greptile on the repo: skip step 5 and rely on whatever review process the repo actually uses.
