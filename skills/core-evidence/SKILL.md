---
name: core-evidence
description: Evidence discipline for any claim, number, fix, speedup, citation or "done" statement. Use before reporting results or finishing a task, when summarizing work, when a subagent reports success, and when wording could overclaim ("novel", "faster", "fixed", "verified").
---

# core-evidence

Every sentence that reports a result carries its evidence, or says it has none. This is the
ecosystem's first rule (`../../../CLAUDE.md` rule 1). It applies to chat replies, LEDGER entries,
notebooks, READMEs and manuscripts alike.

## Label every claim

| label | meaning | what must accompany it |
|---|---|---|
| **MEASURED** | produced by code in this session or recorded in an artifact | the command and the artifact path (`results/*_gates.json`, a log line, a test name) |
| **DERIVED** | follows from stated premises | the premises and the steps, shown |
| **CITED** | stated by a source | the PDF on disk you opened, page and equation/figure number |
| **PREDICTED** | registered before a run | where it was registered (`docs/PLAN.md` sect. N, date) and, later, its score |
| **RECORDED** | taken from an older note, not re-run now | the note's path and date, plus "not re-run" |
| **UNVERIFIED** | believed, not checked | the word itself, and what would check it |

Write the label implicitly ("measured: `pytest -q` -> `<N> passed in <t> s`", quoting the real line) or explicitly; never leave a
reader to guess which one applies.

## Steps before you write the final report

1. **Collect.** List each claim the report makes. Completion: every claim has a label.
2. **Check the strength.** For each claim ask: does the wording exceed the evidence in
   *scope* (data set, geometry, hardware, one seed), *strength* (correlation vs cause, one run vs a
   distribution) or *generality* ("always", "never", "the first")? Narrow the wording until it does not.
3. **Quote, don't paraphrase, the decisive output.** The shortest line that settles it
   (the test runner's summary line, `eps_F = <value>` from the gate JSON), not a paraphrase like "tests look good".
4. **Close with the honesty block** — three lines, always:
   ```
   ran:            <commands / gates actually executed, with results>
   skipped:        <what was not run, and why>
   not verified:   <claims that remain UNVERIFIED / RECORDED>
   ```

## Rules that recur

- **Numbers come from artifacts, never from memory.** A count in a status table is re-measured with
  its date and command, or marked RECORDED.
- **A subagent's "pass" is a claim.** Re-run the gate or spot-check two facts before relying on it
  (`benz:core-delegate`).
- **Negative and unfavourable results stay**, with their cause. A refuted prediction is reported, not deleted.
- **Scope travels with the headline**, in the same sentence: "2-D acoustic, one shot, CPU float64".
- **Speedups are ratios at equal accuracy with an environment row** (`benz:code-fast`).
- **"Novel", "first", "nobody has"** require a recorded prior-art sweep (terms, date, hits); an empty
  web search is weak evidence and is reported as such (`benz:paper-adopt`).
- **Distinguish "the paper claims X" from "we verified X".**
- When evidence is missing and cannot be produced now, say so plainly and stop; do not fill the gap
  with a plausible sentence.
