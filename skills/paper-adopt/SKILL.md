---
name: paper-adopt
description: Decide whether a published method should enter one of Benz's repos (as a bitwise-default add-on or as a separate experiment) by five questions - does it apply to this geometry, what currency does it pay in, can it be a no-op by default, what is the gate, who already published it. Use when a paper is read for adoption, before proposing a method lift into das_ani/uni_fwi_fast or any active repo, and before seeding a new experiment repo.
---

# paper-adopt

Revised from `inspiring_papers/skills/paper-extract` (2026-08-12), generalized beyond das_ani/das_target.
A paper's motivation, data and headline number do not transfer; re-price everything in our terms.
**The default answer is no.** Read the whole paper first (`benz:paper-read`).

## The five questions — in order, stop at the first "no"

1. **Geometry / physics fit.** Write the method's assumptions (isotropic or equipartitioned field, many
   realizations, plane waves, 2-D vs 3-D, acoustic vs elastic, point sensor vs gauge-length strain, uniform
   sampling) and check each against the target repo. Example: F-J's `J0(kr)` assumes isotropy, provably wrong
   for a one-sided vehicle limb. A mismatch is fatal and cheap to find.
2. **Currency.** Re-price the headline in what the target repo actually spends: realizations to a usable
   gather, pick error bar, ridge sharpness, model error at equal cost, wall time at equal accuracy, memory.
   Illegal currencies: dB on an object we never look at, a quantity outside the repo's scope, a ratio without
   an environment row, "looks cleaner".
3. **Bitwise no-op by default?** Yes -> **add-on**: new function or keyword whose default path reproduces
   today's output under `np.array_equal`; write the no-op test AND the runs test first. No -> **experiment**:
   its own repo or a paused-repo branch, extract-never-import. There is no third answer.
4. **Gate before code.** Name the number and the artifact path before implementing (`benz:code-verify`):
   planted answer, downstream product inside its spread, 5th-percentile cosine, both halves of any ratio.
5. **Prior art.** Search before claiming; log the terms, the date and the hits in the repo ledger whether or
   not anything is found; escalate to Benz when a near-hit appears. An empty search is weak evidence.

## Report block (into the repo's LEDGER.md / research ledger)

```
candidate:   <method> (<Author Year>, eqs. <n-m>, PDF <path>)
Q1 geometry: <fits / does not fit: why>
Q2 currency: <re-priced headline>
Q3 additive: <ADD-ON: keyword X default bitwise | EXPERIMENT: where>
Q4 gate:     <number + artifact path>
Q5 prior art:<terms, date, hits>
verdict:     <adopt / decline (with the number) / blocked on ...>   (decision: Benz, YYYY-MM-DD)
```

A declined adoption with a number is a result: record it so it is not reopened.
