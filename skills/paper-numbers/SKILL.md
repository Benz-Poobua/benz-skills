---
name: paper-numbers
description: Number tracing - every number quoted in a manuscript, README, notebook or ledger comes from a gate artifact (results/*_gates.json) through a tracer script that fails on drift; registering a new number in the same change. Use when quoting any number in prose, when results are regenerated, and before compiling or submitting a manuscript.
---

# paper-numbers

A number typed by hand drifts. A traced number fails loudly when its artifact moves.

## Pattern (already in mfold, uni_fwi_fast, uni_fwi, das_mixed, rhess, tfwi, sigGP)

- Experiments write `results/<exp>_gates.json` (named values, with the command that produced them).
- A tracer (`scripts/check_numbers.py` or `scripts/check_paper_numbers.py`; `make check-numbers`) lists, for
  every quoted number: the artifact path, the JSON key, the rounding, and the documents where it appears; it
  exits non-zero on any mismatch, missing artifact or stale rounding, and lists ungated claims by name.
- Manuscripts either quote numbers that the tracer greps, or use placeholders filled by a script
  (e.g. `mypaper/das_grad/scripts/fill_dgmm_numbers.py`, `\NB{...}` macros in ant_fast) with a `--check` mode.

## Steps when you quote a number

1. Find or create its gate artifact (rerun the experiment; never copy a number from chat or memory).
2. Register it in the tracer in the same change (artifact, key, rounding, document).
3. Run the tracer; completion: it reports N/N with the new number included.
4. If the number moved, say why in the LEDGER entry; never silently update prose.

## Traps

- A tracer that scans `CLAUDE.md` breaks when CLAUDE.md is split: add the frozen history file and the
  docs that received the moved text to its document list (done 2026-11-09 in uni_fwi_fast, uni_fwi).
- A rounding change is a drift: record the rounding rule with the number.
- Counts in status lines ("475 tests") are numbers too: re-measure with date and command or label RECORDED.
