---
name: create-readonly-db-role
description: 'Provision a hardened SELECT-only Postgres role so AI agents can safely read a production database. Works on Supabase and any Postgres. Use when the user wants agents to query prod data, says "read-only role", "safe prod DB access for agents", or is tired of running SQL by hand for agents. Differentiator: this skill CREATES the role and wiring; day-to-day querying belongs in a project-local skill.'
---

# Create a Read-Only DB Role for Agents

A pattern used at DeepAPI. A SELECT-only role kills catastrophic writes at the permission level. Residual risks (data leaks, heavy queries) are handled by a denylist and timeouts. Agents stop being blind on prod; the human stops being the SQL bottleneck.

The SQL, timeouts, grants, denylist, RLS setting, role name, and connection steps below are customizable examples for your own system. Adapt them. They are not a copy of any live production setup.

## The pattern — 3 layers

1. **Hard wall — grants.** The role gets SELECT and nothing else. Writes are impossible, not just discouraged.
2. **Denylist, not allowlist.** Grant SELECT on ALL current + future tables in `public` (via default privileges), then revoke tables that hold secrets or PII. Never grant the `auth` schema. Future tables are auto-readable by design; new sensitive tables need a manual revoke.
3. **Soft guardrails.** Example: `default_transaction_read_only = on` plus a short `statement_timeout`. Tune both for your workload.

**RLS trap:** if tables have Row Level Security and no policy mentions the new role, every SELECT returns 0 rows. One common fix is `alter role ... bypassrls` — this only skips row filtering. The SELECT-only grants and denylist still apply. Use it only if it fits your security model.

## Workflow

1. **State-check.** `select rolname from pg_roles where rolname = 'agent_reader';` — if it exists, you are updating, not creating. Replace `agent_reader` with the role name you choose.
2. **Pick the denylist with the human.** Ask which tables hold secrets or PII that agents must never see (credentials, webhook payloads, identity tables).
3. **Write the SQL to a repo file first** (e.g. `docs/database/create-agent-reader-role.sql`) with comments: what / why / how to apply / how to verify / how to revert. Never hand SQL only in chat.
4. **The human applies it** — agents never run DDL on prod. Supabase: paste the whole file into the SQL editor, then DELETE the query from editor history (it contains the password). Store the password in a password manager.
5. **Wire the connection string** through a protected secret manager or local environment configuration. Never commit it. For a Supabase session pooler, the username is typically `<role>.<project-ref>` on port 5432. Install `psql` from your package manager (Homebrew `libpq` on macOS) if it is missing.
6. **Verify** with the loop below.
7. **Write a project-local usage skill** so future agents know the key tables, query patterns, and hard rules (read-only forever, never paste PII into commits/docs).

## SQL template

```sql
-- Example only. Rename the role, timeout, and denylist for your system.

-- 1. role + soft guardrails
create role agent_reader with login password 'REPLACE_ME';
alter role agent_reader set default_transaction_read_only = on;
alter role agent_reader set statement_timeout = '10s';  -- example timeout; change as needed

-- 2. SELECT-only grants, denylist model
grant usage on schema public to agent_reader;
grant select on all tables in schema public to agent_reader;
alter default privileges for role postgres in schema public
  grant select on tables to agent_reader;   -- future tables auto-readable

-- 3. denylist: keep secrets and PII invisible (replace with your own tables)
revoke select on table public.secrets from agent_reader;
revoke select on table public.private_events from agent_reader;

-- 4. only if RLS is enabled, no policy covers this role, and bypass fits your model
alter role agent_reader bypassrls;
```

Revert: `drop owned by agent_reader; drop role agent_reader;`

## Verification loop (all must pass before declaring done)

```bash
# Load the connection URL from your secret manager or local environment configuration.
psql "<readonly-connection-url>" -X -c "select current_user;"                      # -> agent_reader
psql "<readonly-connection-url>" -X -c "show statement_timeout;"                   # -> matches your chosen timeout
psql "<readonly-connection-url>" -X -c "select count(*) from public.<big_table>;"  # -> real number, NOT 0
psql "<readonly-connection-url>" -X -c "delete from public.<any_table> where false;"
# -> ERROR: read-only transaction (soft guardrail)
psql "<readonly-connection-url>" -X -c "begin; set transaction read write; delete from public.<any_table> where false; rollback;"
# -> ERROR: permission denied (the hard wall)
psql "<readonly-connection-url>" -X -c "select * from public.<denylisted> limit 1;"         # -> ERROR: permission denied
psql "<readonly-connection-url>" -X -c "select * from auth.<identity_table> limit 1;"       # -> ERROR: permission denied
```

Writes must be blocked **twice over**: once by the read-only guardrail, and again by `permission denied` with the guardrail off. If any check fails, fix the grants and re-run ALL checks.

## Failure modes

- **Every table returns 0 rows** → RLS is enabled and the role has no policy → consider `bypassrls` (step 4 of template) only if it fits your model.
- **A write succeeded during verification** → grants are wrong. Stop, revoke everything, re-run the template.
- **Supabase auth failed** → pooler username is usually `<role>.<project-ref>`, not the bare role name.
- **`statement timeout` on legit queries** → query too heavy; add filters/limits. Do not raise the timeout as a first resort.

## Maintenance

- New sensitive table → add a `revoke select` next to the denylist block.
- Rotate password: `alter role agent_reader with password '...'` then update the secret in your secret manager or local environment configuration.
- Never let agents write through this role. Prod writes stay human-only.
