# benz-skills — sources, licences and what each skill prevents

Read on 2026-11-09. External material was adapted (MIT/Apache, with attribution) or used for ideas only
(no licence file); Benz's own repositories (MIT) were copied freely.

## External sources

| source | licence (read from file) | used for |
|---|---|---|
| `useful_agents/skills` (mattpocock/skills @ 4ae2317) | MIT, (c) 2026 Matt Pocock | `code-debug` (diagnosing-bugs loop), `code-review` (two-axis review), `writing-for-agents` principles applied to every SKILL.md (context pointers, leading words, progressive disclosure, completion criteria, single source of truth), `core-long-run` hand-over idea (wizard) |
| `useful_agents/9arm-skills` (thananon/9arm-skills @ a1fc303) | **no licence file** | ideas only, re-written: debug-mantra -> `code-debug`; scrutinize -> `code-review`; qwen-agent/qwenchance -> `core-delegate` (cheap-worker delegation, context budget, handoff). The older uni_fwi skills fwi-delegate/fwi-scrutinize had already adapted these. |
| `useful_agents/agentskills` (agentskills/agentskills @ 83021e2) | Apache-2.0 | SKILL.md format (frontmatter, references/ scripts/ assets/, progressive disclosure) |
| `useful_agents/pi`, `useful_agents/pi-lens` | MIT | practices only (distilled 2026-11-09): capped hand-backs and output-to-file, model routing by task type, leaf agents cannot spawn agents, delegation contract (paths, acceptance, non-goals, git authority), "never run" git list, honesty labels (ran / skipped / unconfirmed), net-count rule for process rules, read-before-edit, CLAUDE.md = rules only |
| Claude Code docs (skills, sub-agents, plugin marketplaces, memory), fetched 2026-11-09 | — | discovery rules: project skills stop at the git root; user-scope plugin works everywhere; CLAUDE.md loads from every ancestor directory. Tested 2026-11-10: the install COPIES the plugin into `~/.claude/plugins/cache/`; `claude plugin update` refreshes it only after a version bump (the docs' "read live" did not hold here) |
| caveman plugin (JuliusBrussee/caveman @ 0d95a81) | MIT, (c) 2026 Julius Brussee | companion plugin, not vendored; install.sh installs it |

## Benz's own material (MIT) merged here

| from | into |
|---|---|
| `das_ani/CLAUDE.md` sect. 5, `das_ani/src/{utils,plots}.py`, `submit.sh`, `slurm/` | `code-house-style` (+ verbatim `load_config`/`get_cfg`, rcParams), `code-hpc` |
| `uni_fwi/skills/{fwi-delegate,fwi-scrutinize,fwi-fidelity}` | `core-delegate`, `code-review`, `code-verify` |
| `mfold/skills/{paper-writing,research-ledger}`, `myarchive/rhess/skills/paper-writing`, `myarchive/tfwi/skills/fwi-paper` | `paper-write`, `core-ledger` |
| `mypaper/mybible/skills/{book-verify,book-figures,book-ledger}` | referenced (kept in mybible), conventions summarized in `paper-bib`, `paper-figures` |
| `inspiring_papers/skills/paper-extract` | `paper-adopt` (generalized) |
| `mfold/scripts/guard.py`, `mfold/scripts/_common.py::resumable_map`, `sigGP/src/workflow.py` | `core-long-run` (guard copied verbatim; the others referenced) |
| per-repo `research-ledger` skills (10 copies) | `core-ledger` (repo copies keep their repo-specific numbering; generic text now lives here) |

## What each skill prevents (net-count rule)

| skill | mistake or cost it prevents (observed in this ecosystem) |
|---|---|
| core-evidence | quoted counts that were recalled, not measured; "pass" from a subagent taken as fact |
| core-delegate | 8 parallel agents hitting the 5-hour limit (2026-11-09); pasted reports flooding context |
| core-ledger | 1900-line CLAUDE.md files loaded in every session; status lost between sessions |
| core-long-run | sweeps starved by Low Power Mode / clamshell sleep; runs lost on account switch; orphans after pkill |
| code-house-style | divergent configs/plots across repos; MPS failures; TF32 silently on |
| code-verify | finite-but-wrong outputs, silent zero gradients, guessed tolerances, vacuous bitwise "refactors" |
| code-fast | speedups measured at unequal accuracy; symlinked inputs measuring 4 records instead of 96 |
| code-debug | fixes before a reproducer; theory-first debugging |
| code-review | rubber-stamp reviews; unmeasured optimizations merged |
| code-notebooks | hand-edited generated notebooks; claims without asserts; stale outputs |
| code-extract | GPL/no-licence code copied into MIT repos; cross-repo imports |
| code-hpc | jobs dying without logs; partial stacks exiting 0; wrong config preflighted |
| paper-read | skimmed citations; signs read from pdftotext |
| paper-bib | ghost keys, duplicate PDFs under two names, guessed bib fields |
| paper-write | unpublished results in the book; novelty without a sweep |
| paper-numbers | hand-typed numbers drifting from artifacts |
| paper-figures | figures that cannot be regenerated |
| paper-adopt | methods lifted without a geometry check or a gate |
