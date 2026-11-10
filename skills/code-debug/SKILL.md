---
name: code-debug
description: Systematic debugging for wrong numbers, crashes, hangs and slowdowns - build a tight red loop first, reproduce and minimise, rank falsifiable hypotheses, change one variable at a time, regression test before the fix, record the root cause. Use when something is broken, failing, throwing, hanging, slow, or "the numbers look off".
---

# code-debug

Adapted from mattpocock/skills `diagnosing-bugs` (MIT) and the ideas of 9arm-skills `debug-mantra`
(no licence file: ideas only, re-written). Credit in `docs/SOURCES.md`.

## Phase 1 — a tight red loop (this is the skill)

Build ONE command that drives the real code path and asserts the exact symptom: a failing test, a CLI
call on a fixture diffed against a known-good output, a differential run (old vs new commit, float32 vs
float64, backend A vs B), a bisection harness (`git bisect run`), or a seeded property loop for
intermittent failures. Make it fast (seconds), deterministic (seeds, pinned threads) and red-capable.
**Completion: you have run it once and shown its red output.** No loop, no hypotheses — if you cannot
build one, say what you tried and ask Benz for the missing artifact.

## Phase 2 — reproduce and minimise

Confirm it fails the way Benz described (wrong bug = wrong fix). Shrink inputs, channels, steps and config
one cut at a time until every remaining element is load-bearing.

## Phase 3 — 3-5 ranked, falsifiable hypotheses

Format: "If X is the cause, changing Y makes it disappear / changing Z makes it worse." Show the list before
testing when Benz is present; he often re-ranks instantly.

Numerical suspects to always consider: sign/lag/Fourier convention; units and sampling rate (raw vs
processed); axis order `(nz,nx)` vs `(nx,nz)`, C vs Fortran order; dtype (float32 accumulation depth);
a config key that nothing reads; non-finite values laundered to finite; tolerance absolute where it should be
relative; CFL/dispersion limits; boundary/sponge placement; a stale wheel or env (`assert_own_src()`:
another repo's flat `src` on `sys.path`).

## Phase 4 — instrument, one variable at a time

Debugger/REPL first; otherwise targeted logs tagged `[DEBUG-xxxx]` so cleanup is one grep. For slowdowns:
baseline timing, then bisect — measure first, fix second (`benz:code-fast`).

## Phase 5 — regression test, then fix

Turn the minimised repro into a test at the seam where the bug lives; watch it fail on the current code;
fix; watch it pass; re-run the original loop. If no honest seam exists, record that as a finding.

## Phase 6 — clean up and record

Remove `[DEBUG-` lines and throwaway harnesses; write the root cause, mechanism, fix, validation and why it
slipped through in `LEDGER.md` (the post-mortem); add a trap line to the repo's `CLAUDE.md` sect. 8 when the
lesson is durable.
