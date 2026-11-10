---
name: paper-write
description: Honest scientific writing for Benz's manuscripts and books - book first (the FWI Book takes published work only, then the project paper), no hallucination or ghost citations, math derived step by step, every number traced, scope beside the headline, refuted predictions stated, numbered future work. Use whenever manuscript, book, abstract, caption, cover-letter or report text is written or revised.
---

# paper-write

Manuscripts live in `mypaper/` (one git repo, no remote); the knowledge base is `mypaper/mybible`
(FWI Book `main.tex`, CS Book `siggp.tex`). Prose here is normal academic English (the terse chat style
never enters a manuscript).

## Book first, published work only

1. A **published** method or result enters the FWI Book first (`mypaper/mybible/main.tex`), with its PDF read
   and its bib entry checked (`benz:paper-read`, `benz:paper-bib`), and the book's gates green
   (`mypaper/mybible/skills/book-verify`).
2. Only then does a project manuscript cite or build on it.
3. **Unpublished results of Benz's projects never go into the books** (Benz, 2026-09-22); they live only in
   the project manuscripts until published.

## Steps for any section

1. **Experiments first**: every number comes from a gate artifact; no number without a gate
   (`benz:paper-numbers`).
2. **Define, derive, then measure**: define every symbol at first use; derive equations step by step
   with numbered equations and stated assumptions; give the conventions (Fourier sign, units, geometry);
   then show the measurement.
3. **Cite as you write**: natbib only (`\citet`, `\citep`); every key held and read; page/eq pointers only
   when verified on the page; the book cited by `\label`.
4. **Scope beside the headline**: data set, geometry, dimension, hardware, precision, number of seeds —
   in the same sentence or box as the claim.
5. **Separate ours from reproduced**: what is the authors' result, what we re-derived, what is new.
6. **Negative results and refuted predictions stay in the text**, with their cause.
7. **Novelty language only after a recorded prior-art sweep** (terms, date, hits; `benz:paper-adopt` Q5).
8. **Future work is numbered**, each item with a deliverable and the condition that would kill it.

## Before handing a draft over

- Back up before a large edit: `<dir>/archive/<name>_before_<pass>.tex`.
- Compile (tectonic): 0 errors, 0 undefined references and citations; check overfull boxes.
- Run the manuscript's number tracer and citation check; report results as numbers.
- Report what changed, what was verified, what remains UNVERIFIED (`benz:core-evidence`).
