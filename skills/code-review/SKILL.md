---
name: code-review
description: Outsider review of a diff, branch, module or a claimed result (speedup, fix, "matches the paper", "publishable") - question the premise, trace the real path across seams, verify at equal accuracy, check house style and gates, report severity-ordered findings with evidence. Use when asked to review, audit or sanity-check, and before merging a change to code that produced published numbers.
---

# code-review

Adapted from uni_fwi `skills/fwi-scrutinize`, mattpocock/skills `code-review` (MIT) and the ideas of
9arm-skills `scrutinize` (no licence file: ideas only). For an independent second opinion on an
important change, delegate to the `benz:verifier` agent (opus) with the diff path and the claim.

## Stance

Read cold. End to end, not diff-local. Every finding carries evidence (a path:line, a trace step, a
number). No rubber stamps: "LGTM" without saying what you traced is not output.

## Steps

1. **Blind pass first.** Write your own findings before reading the author's summary or any bot output.
2. **Intent and premise.** State the change's goal in one sentence (if you cannot, stop: underspecified).
   Was the bottleneck or bug measured? Is there a simpler change with the same effect? (One
   simpler-alternative pass is mandatory unless Benz said not to question scope.)
3. **Trace the path.** Config key -> parser -> function -> kernel -> output file. Mark the seams where bugs
   hide: precision casts, checkpoint/replay boundaries, chunk edges, channel windows (absolute vs relative
   indices), sign/lag conventions, resume/skip logic, multiprocessing start method, default values.
4. **Verify the claim.** Speedups at equal accuracy with an environment row (`benz:code-fast`); fixes with a
   gate that fails on the parent (`benz:code-verify`); "matches the paper" against the PDF page and equation
   (`benz:paper-read`). Unverified claims are reported as hypotheses.
5. **Standards.** House style (`benz:code-house-style`): headers, config helpers, rcParams, no MPS, TF32
   pinned, provenance headers on extracted code, generated notebooks untouched by hand.
6. **Silent behaviour changes.** Defaults, file names (load-bearing grammar), published numbers, legacy
   switches, deleted gates, changed tolerances, new dependencies, anything in another repo's copy.
7. **Report.** Severity-ordered: blocker -> major -> minor -> nit. Each: finding (one sentence, `path:line`),
   why it matters, evidence, minimal fix. End with a verdict (ship / fix-then-ship / rework / reject) and the
   single biggest reason.
