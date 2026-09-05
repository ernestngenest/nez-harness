---
name: agentic-productivity-setup
description: 'Build or rebuild a private, local-first macOS system that measures daily Git commits, active AI-agent sessions, and instruction prompts, then sends aggregate charts to Discord. Use when someone asks to set up an agentic productivity tracker, install daily agent reports, recreate this architecture on a Mac, or understand how to build it safely. Differentiator: creates a fresh system from generic contracts and never copies another person''s data, paths, credentials, repositories, prompts, or private configuration.'
---

# Agentic Productivity Setup

Build a deterministic system that measures whether AI agents increase a
person's output over time. Keep collection local. Send one private Discord
report each morning with exactly three aggregate charts.

## Privacy rules

Treat these as hard requirements:

1. Build a fresh implementation. Never copy another installation, runtime
   database, log, session store, credential, machine path, repository list, or
   private configuration.
2. Never persist or transmit prompt text, responses, tool output, repository
   names, file paths, identities, raw session IDs, or commit messages.
3. Read native agent stores only to count events. Keep temporary identifiers in
   memory, then discard them. Persist a one-way hash only when a collector needs
   a cross-run baseline.
4. Render charts locally by default. Only Discord should receive the daily
   totals and chart images. Explain the exact data flow before enabling any
   optional remote chart service.
5. Store the Discord webhook in the current user's macOS Keychain.
   Never put it in source code, a command argument, an environment file, the
   database, logs, tests, or the scheduler definition.
6. Use synthetic fixtures in tests. Never use copied session data, real prompts,
   real repository metadata, or live credentials.
7. Open native databases read-only. Collectors must not modify agent state.
8. Report missing, unreadable, or unsupported sources as coverage problems.
   Never turn collection failure into a silent zero.

## Confirm the scope

First determine whether the user wants an explanation, a new project, or an
installation. Do not create or install anything when they only asked how it
works.

For a build, confirm or safely default these values:

- Platform: macOS. Ask before adapting the design to another operating system.
- Code root: `$HOME/code`.
- Timezone: the Mac's configured timezone.
- Report time: 08:00 local time.
- Report window: 90 days ending yesterday.
- Agent harnesses: only tools the user wants measured.
- Project location and reverse-DNS LaunchAgent label.

Do not ask the user to paste a webhook into chat. Configure it through secure
terminal input after the application is built.

Ask before changing metric definitions, storage boundaries, report
destinations, or data sent off the Mac. Record consequential choices in a short
ADR inside the generated project.

## Architecture

Use this data flow:

```text
Git reflogs + native agent registries
    -> read-only collectors
    -> daily aggregate counts
    -> local SQLite database
    -> local chart renderer
    -> one Discord webhook request
```

Keep the source checkout separate from the installed runtime:

- Copy application code into `~/Library/Application Support/<app>/app/`.
- Store aggregate state beside it in `metrics.sqlite3`.
- Store logs in `~/Library/Logs/<app>/`.
- Install the plist in `~/Library/LaunchAgents/`.
- Give directories mode `0700` and sensitive files mode `0600`.
- Preserve aggregate state across reinstalls and normal uninstalls.

## Metric contracts

Implement three independent metrics. Do not create a combined productivity
score.

### Unique local commits

- Discover Git repositories recursively under the configured code root.
- Deduplicate primary checkouts and linked worktrees by Git common directory.
- Read local creation events from reflogs for the requested date range.
- Include only commits whose author or committer email matches an identity
  configured in that repository.
- Count each commit hash once across all refs and worktrees.
- Exclude fetched commits, pushes, and branch movement by themselves.
- Keep hashes in memory only. Store the final daily count.

### Active agent sessions

- Count one session on each local calendar day where its native registry records
  activity.
- Include GUI, CLI, headless, resumed, parent, subagent, delegated, and automated
  sessions.
- Deduplicate with the harness's native session identity in memory.
- Keep each harness separate in storage and reports.

### Instruction-bearing prompts

- Count stored user, system, and developer inputs that contain instructions.
- Include human prompts, automation, setup context, delegation, and subagent
  instructions.
- Exclude assistant responses, tool results, empty inputs, and duplicated storage
  copies.
- Inspect content only long enough to classify the event. Never store or log it.

Convert every timestamp into the configured timezone before assigning a day.

## Collector design

Use one adapter per harness. Prefer native registries over process inspection,
shell history, window titles, or guessed file timestamps.

Support common source shapes:

- JSON or JSONL session records.
- Read-only SQLite registries.
- Editor global or workspace state databases.
- Authenticated native CLI export when no readable local registry exists.

Each adapter must return:

- daily unique session identities in memory;
- daily prompt counts;
- `full`, `partial`, `unavailable`, `absent`, or `error` coverage;
- a short detail string containing counts and limitations, never private data.

Some stores expose a session total but no timestamp for each turn. For those
stores, save a hashed source key and total, then attribute only positive deltas
observed after the local baseline. Mark older attribution as partial.

Discover installed harnesses at runtime. Keep unsupported tools absent from the
chart, not mislabeled as zero activity.

## Aggregate database

Use SQLite in WAL mode. Keep the schema small:

- `daily_metrics`: day, metric, harness, count, collection time.
- `collector_health`: installation and coverage state per harness.
- `source_snapshots`: hashed source key, last total, observation time.
- `collector_baselines`: first reliable observation per harness.
- `deliveries`: report day, sending state, sent time, and a short safe error.

Use monotonic upserts for daily counts. A later incomplete scan must not erase a
higher value already stored.

Never create tables for raw events, messages, prompts, responses, repository
names, paths, or identities.

## Report and Discord delivery

Build exactly three charts for the selected window:

1. Daily unique commits as a line and area chart.
2. Daily active sessions as stacked bars split by harness.
3. Daily instruction prompts as stacked bars split by harness.

Add a straight ordinary least-squares trendline to each chart. Use combined
daily totals for the session and prompt trendlines. Render PNG files locally
with a pinned charting dependency. Never silently fall back to a network
renderer.

The Discord message should contain only:

- the report day;
- yesterday's three totals;
- a short collector coverage summary;
- the three PNG attachments.

Send one multipart POST. Disable allowed mentions. Accept only valid Discord
webhook hosts. Use a short timeout. Never log the request URL or body.

Claim the report day in SQLite before network work. Mark it sent only after a
successful Discord response. Normal runs must send once per report day. Require
an explicit force option to resend.

## Scheduling

Use a user LaunchAgent. Do not run an LLM on the schedule.

Configure:

- `StartCalendarInterval` for the chosen daily report time.
- `StartInterval` of 300 seconds when a collector needs prompt deltas.
- `RunAtLoad` for login and wake catch-up.
- `ProcessType` set to `Background`.
- `LowPriorityIO` enabled.
- A restrictive `077` umask, represented as decimal `63` in the plist.
- stdout and stderr paths inside the private log directory.

Every interval may observe delta-only sources. Before the report time, stop
after that local observation. At or after the report time, collect yesterday,
build the full window, and send only if that day is not already marked sent.

The installer must render absolute runtime paths into the plist, validate it
with `plutil`, replace the existing job safely, and start it. Keep credentials
out of the plist.

## Project shape

Use a small, readable project:

```text
agentic_productivity/
  cli.py
  collectors.py
  database.py
  model.py
  reporting.py
bin/
  agentic-productivity
launchd/
  <label>.plist.in
scripts/
  install.sh
  uninstall.sh
  test.sh
tests/
docs/adr/
```

Use Python 3.11 or newer unless the user chooses another simple, maintainable
stack. Keep collectors modular. Keep the scheduled command deterministic and
non-interactive.

Provide these commands:

- `doctor`: check prerequisites, paths, credential presence, database, and
  collector coverage without exposing secrets.
- `collect`: collect and store aggregates without delivery.
- `mock`: run collection, reporting, chart rendering, and multipart assembly
  without network access or delivery state.
- `run`: perform the scheduled observation and idempotent report.
- `status`: show safe collection and delivery state.
- `configure-webhook`: read the webhook from standard input and store it in
  macOS Keychain.

## Secure webhook setup

Use an interactive shell pattern like this after implementation:

```sh
read -r -s REPORT_WEBHOOK
printf '%s\n' "$REPORT_WEBHOOK" | ./bin/agentic-productivity configure-webhook
unset REPORT_WEBHOOK
```

The command must print only whether configuration succeeded. It must never echo
the secret.

## Verification gate

Do not report success until all checks pass:

1. Test every collector with synthetic native-store fixtures.
2. Test deduplication, timezone boundaries, prompt-role filtering, monotonic
   upserts, coverage failures, and idempotent delivery.
3. Test that reports contain only aggregates and exactly three attachments.
4. Run the full test suite and the network-free `mock` command.
5. Install into a temporary home first. Confirm no source checkout or runtime
   state is required for execution.
6. Verify the rendered plist contains no credential or private source data.
7. Verify tracked files contain no databases, logs, session exports, prompt
   fixtures, credentials, machine-specific absolute paths, or real identities.
8. Run `doctor`, load the LaunchAgent, and confirm its last exit status is zero.
9. Send a live test report only with the user's permission.

If any privacy check is uncertain, stop the release of that file. Do not weaken
the check.

## Completion report

Tell the user:

- where the source, installed app, aggregate database, plist, and logs live;
- which metrics and harnesses are enabled;
- the timezone, report time, and window;
- whether the webhook is configured, without showing it;
- which tests ran and whether the LaunchAgent is healthy;
- every partial or unavailable collector that still matters.
