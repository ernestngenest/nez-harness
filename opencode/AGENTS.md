# OpenCode — Global Rules
# Stack: JavaScript · Vue · Django · React Native · React · Next.js

Follow all rules below for every file you generate or edit.
Goal: clean code, zero smell, zero duplicate, best practices, PR-ready.

## ⚠️ Scope Rules — Read This First

These rules **only apply to:**
- ✅ New files / functions you create in this session
- ✅ Lines of code you directly touch / edit

These rules **do NOT apply to:**
- ❌ Existing code you are not changing — **leave it alone**
- ❌ Files owned by other team members outside your task scope
- ❌ Code outside the scope of the requested change

**Specifically:**
- If asked to edit `handleSubmit()` → only fix `handleSubmit()`, do not refactor other functions in the same file
- If you spot a smell in someone else's code → **ignore it, do not auto-fix**
- Never delete or rename anything that is not part of the current task

---

## Karpathy Guidelines

Source: [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop, name what's confusing, and ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions your changes made unused; don't remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"
- For multi-step tasks, state a brief plan with a verify step per item.

---

## Universal Rules (all stacks)

### Single Responsibility Principle (SRP)
Every unit of code must have **one reason to change**. Apply at all levels:

- **Function** — does one thing only. If the name needs "and" or "or", split it.
- **File/Module** — groups one concern (e.g. `userService.js` handles user logic only, not auth + email + formatting).
- **Component** — renders one piece of UI. Extract sub-components when a component handles both display logic and data fetching.
- **Class/Model** — owns one domain concept. No God classes.

**Red flags that signal SRP violation:**
- Function name contains `and` / `or` / `also` → split it
- File imports from 4+ unrelated domains → split the file
- Component does API call + maps data + renders UI → extract a service layer or custom hook
- A change to business logic breaks the UI layer → missing separation

### Functions
- Max **20 lines** per function/method → Extract Function if longer
- Max **3 parameters** → use an object/dict if more
- One function, one responsibility (see SRP above)
- Descriptive names: `getUserById` not `getData`

### Duplicate Code
- Block > 5 lines appearing 2+ times → must extract
- Before writing new logic, check if a utility already exists
- DRY: Don't Repeat Yourself — always

### Dead Code
- Never leave commented-out code
- Never leave unused imports or variables

### Naming
- Variables/functions: `camelCase` (JS/TS), `snake_case` (Python)
- Constants: `SCREAMING_SNAKE_CASE`
- Booleans: prefix `is`, `has`, `can` → `isLoading`, `hasError`
- Avoid generic names: `data`, `temp`, `obj`, `x`

### JavaScript / TypeScript (universal)
- Always `const` by default, `let` only when reassignment needed, **no `var`**
- Early return over nested if blocks
- Use optional chaining `?.` and nullish coalescing `??`
- Error handling required in all async functions
- Utility functions used in > 1 file → put in `utils/` or `helpers/`

---

## Stack-Specific Rules

Load the relevant file before generating code for that stack:

| Working on | Read before coding |
|---|---|
| Vue components / composables | `~/.config/opencode/docs/vue.md` |
| Django views / models / APIs | `~/.config/opencode/docs/django.md` |
| React components / hooks | `~/.config/opencode/docs/react.md` |
| Next.js pages / app router | `~/.config/opencode/docs/nextjs.md` |
| React Native screens / styles | `~/.config/opencode/docs/react-native.md` |

---

## Pre-generation Checklist

- [ ] Same function already exists in codebase? Don't duplicate
- [ ] Function will exceed 20 lines? Plan the split upfront
- [ ] More than 3 parameters? Use an object
- [ ] Any reusable logic? Extract it now
- [ ] All imports used?
- [ ] Any dead / commented-out code?
- [ ] Does this function/file/component do more than one thing? (SRP check) → split before writing

---

## PR Readiness

Code is PR-ready when:
- Zero functions > 20 lines
- Zero duplicate blocks > 5 lines
- Zero unused imports/variables
- Zero inline styles (React Native)
- Zero logic in Vue templates that could be computed
- Zero business logic in Django views
- Zero unnecessary `use client` in Next.js
- Zero manual `useEffect` fetches where Server Component / React Query would do
- Zero props drilling > 2 levels
- Zero SRP violations: no function/file/component doing more than one job
