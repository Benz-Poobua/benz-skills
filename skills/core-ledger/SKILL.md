---
name: core-ledger
description: The working-file discipline every repo follows - CLAUDE.md holds rules only, TASKS.md says where to start, LEDGER.md records what was done (newest on top). Use at the end of every work block, before any commit, when starting cold in a repo, when a task changes state, and when creating or splitting a CLAUDE.md.
---

# core-ledger

A new session must be able to resume from three files: `CLAUDE.md` (rules), `TASKS.md` (top block +
restart prompt) and the newest `LEDGER.md` entry. Nothing is status until it is written there.

## The three working files (same names in every repo)

| file | holds | changes |
|---|---|---|
| `CLAUDE.md` | what the repo is, hard rules, layout, how to run, conventions, gates, licences, traps | only when a rule, the layout or a convention changes |
| `TASKS.md` | "Start here" block, open items (id, task, state, source), restart prompt | every work block |
| `LEDGER.md` | dated entries, newest on top: what changed, numbers with gate paths, failures, decisions | append on top; never rewrite history |

Supporting: `docs/PLAN.md` (hypotheses, registered predictions, kill conditions), `docs/RESULTS.md`
(measured / refuted), `docs/research_ledger.md` (numbered scientific addenda, where a repo keeps one),
`docs/history/` (frozen pre-split copies; never edited). Templates: `references/`.

## When starting cold

Read `CLAUDE.md` -> `TASKS.md` top block -> newest `LEDGER.md` entry. Then run the repo's first
command (usually its test suite) before changing anything.

## End-of-block checklist (in order)

1. Run the repo's gates (`make test`, `make lint`, `make check-numbers` where it exists). Note results as numbers.
2. Prepend a `LEDGER.md` entry (`references/ledger_entry.md`): question, what changed (paths), gate
   results, numbers with artifact paths, scope, failures, decisions with Benz's words and date, NEXT.
3. Update `TASKS.md`: top block, item states, restart prompt.
4. Update `docs/RESULTS.md` / `docs/PLAN.md` if a result or prediction moved.
5. Touch `CLAUDE.md` only if a rule changed, and say so in the ledger entry.
6. If the repo's state word changed (active / paused / retired), update its line in the root `STATUS.md`.
7. Commit only when Benz asks: `git add <paths>`, never `-A` or `.`.

Completion: a fresh session reading the three files would take the same next action you would.

## Rules

- **Predictions before runs.** A study gets predictions and kill conditions in `docs/PLAN.md` before it
  runs; the ledger scores them afterwards, failures included.
- **Refuted results are kept**, with their cause, and never re-asserted.
- **Facts, not intentions**: "converted ch. 15-22, 214 citations" not "worked on citations".
- **Dates are absolute** (2026-11-09), never "today" or "last week".
- **CLAUDE.md stays short** (target <= 200 lines): no dates, counts, speedups or "NOT committed" notes in it.
  Run `python3 <this skill>/scripts/check_doc_paths.py <repo>/CLAUDE.md` after editing it: every
  backticked path must exist.
- **Splitting an old CLAUDE.md:** freeze a verbatim copy in `docs/history/` first, then move dated blocks
  to `LEDGER.md` and plans to `TASKS.md`/`docs/` with `sed` line ranges (never retype), then write the new
  rules file from `references/CLAUDE_template.md`.
