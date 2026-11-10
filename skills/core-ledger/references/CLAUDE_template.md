# <repo> — RULES, LAYOUT, CONVENTIONS (read first, every session)

> **<one-sentence what>.** Status: **ACTIVE** | **PAUSED** (in `myarchive/`; resume only on Benz's request) | **TO BE RETIRED** (-> `<successor>`).
> This file changes only when a rule, the layout or a convention changes. Dynamic state:
> * `TASKS.md` — where to start, open items, restart prompt.
> * `LEDGER.md` — dated record, newest on top.  (+ `docs/research_ledger.md`: numbered scientific addenda, if kept)
> * `docs/...` — <plan / results / notes, one line each>
> Ecosystem rules: `../CLAUDE.md` (auto-loaded). Skills: plugin `benz` (`../benz-skills/PATHS.md`); repo skills: `skills/<name>/`.
> Pre-split text: `docs/history/CLAUDE_until_<date>.md` (frozen).

Owner: Benz Poobua (spoobua@stanford.edu), Stanford Geophysics / SEP. Manuscript: `../mypaper/<dir>/` or none.

---

## 0. What this repository is (one paragraph)

## 1. Working files

| file | holds | changes when |
|---|---|---|
| `CLAUDE.md` | rules, layout, conventions, gates, licences, traps | a rule changes |
| `TASKS.md` | where to start, open items, restart prompt | every work block |
| `LEDGER.md` | dated record | append, newest on top |

## 2. Hard rules
1. <repo-specific rule; reference ecosystem rules by number only when adding detail>

## 3. Layout
```
<repo>/
  src/ ...
```

## 4. How to run
```bash
source <env>/bin/activate        # or ./<env>/bin/python
pytest -q                        # always first
make <targets>
```

## 5. Conventions
(Only deltas from the house style: `../das_ani/CLAUDE.md` sect. 5, skill `benz:code-house-style`.)

## 6. Gates
(Metrics, tolerances and the scripts that decide "correct".)

## 7. Sources and licences

| source | licence | rule here |
|---|---|---|

## 8. Traps
* <symptom> — <cause> — <fix> (LEDGER <date> / history sect. N)
