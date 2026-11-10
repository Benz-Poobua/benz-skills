# LEDGER entry format (prepend under the file title; newest on top)

```
## YYYY-MM-DD — <short title> (session N, optional)

- **Question / request:** <what was asked; quote Benz when it is a decision>
- **Changed:** <paths, one per line or comma-separated; "docs only" when no code moved>
- **Gates:** <command -> result, as numbers>  e.g. `pytest -q` -> 475 passed; `make check-numbers` -> 112/112
- **Numbers:** <value> (<artifact path>) ... each with scope (data, geometry, hardware, precision)
- **Predictions:** <registered where; scored: held / failed, with the number>
- **Failed / not done:** <what did not work or was skipped, and why>
- **Decisions:** <decision> (Benz, YYYY-MM-DD: "<words>")
- **NEXT:** <the single most useful next action>
```

Rules: facts, not intentions; absolute dates; a correction references the entry it corrects and never
rewrites it; numbers that a paper will quote are registered in the repo's number tracer in the same change.
