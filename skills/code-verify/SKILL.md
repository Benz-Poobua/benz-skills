---
name: code-verify
description: Numerical correctness gates for research code - analytic/planted answers, dot-product tests, finite-difference gradient checks, drift and bitwise-refactor gates, tolerance calibration against the one-ULP control, 5th-percentile cosine, downstream-product checks. Use whenever a kernel, operator, adjoint, preprocessing step or refactor changes, before trusting any new number, and before an optimization.
---

# code-verify

No claim without a gate, and every gate emits a number. "Looks right" is not a result. Check the
logic first: write down what the code path computes (the math, the convention, the units) and compare it
with the derivation or the paper **before** testing or optimizing it.

## Pick the gates that apply

| change | gate | pass criterion |
|---|---|---|
| any physics kernel | **analytic / planted answer** (arrival time `d/c`, Green's function, a synthetic with a planted `c(f)`, a planted dv/v) | returns the planted value within a stated tolerance |
| linear operator pair `A`, `A^T` | **dot-product test**: `|<Ax,y> - <x,A^T y>| / (|Ax||y|)` | ~1e-15 float64, ~1e-6 float32 |
| gradient / hand-written adjoint | **central finite differences** over a step sweep (`h` = 1e-2 ... 1e-8), float64; plus equality with autograd | relative error at the best `h` far below 1e-3; autograd match ~1e-15 |
| port of an existing implementation | **drift gate** against the reference run in its own env (subprocess, never import) | bitwise, or within the calibrated tolerance |
| refactor / speed-up claimed bitwise | `np.array_equal` on outputs over every mode x geometry | identical; if not, it is not a refactor |
| new optional feature | **no-op test** (default path bitwise unchanged) AND **runs test** (the new path is reached) | both; a knob the code never reaches reports "bitwise identical" |
| precision / tolerance claim | **one-ULP control**: the same reference in float32 vs float64 | the new error stated as a multiple of the control (e.g. 0.45x) |
| array-wide fidelity | rel. Frobenius `eps_F` + per-trace cosine divergence **at the 5th percentile, never the mean** + SSIM of dispersion images (das_ani `src/error.py`) | numbers recorded |
| anything feeding a scientific product | **judge the downstream product** (picked curve, image, inverted model) against its own measurement spread | inside the spread |
| copied code | **standalone AST gate** (`tests/test_standalone.py`): no cross-repo imports, no `sys.path` hacks | passes |

## Steps

1. **Logic check**: read the path end to end; state the computed quantity in math; list conventions
   (Fourier sign `e^{+iwt}`, lag sign "positive = source -> receiver", units, `(nz,nx)` vs `(nx,nz)`,
   C vs Fortran order). Completion: a short written statement the gate can falsify.
2. **Calibrate the tolerance before running the gate**: measure the reference's own float32-vs-float64
   difference; never guess `1e-6`. An absolute tolerance in physical FWI units is meaningless (scale
   footgun, recorded six times in this ecosystem) — use relative or scale-aware tolerances.
3. **Write the gate first** (red on the parent when it tests a fix), then the change.
4. **Mutate the gate once**: break the code deliberately and watch the gate go red, then restore it.
5. **Record**: the gate writes its number to `results/<name>_gates.json`; tests assert it; numbers quoted
   anywhere go through the number tracer (`benz:paper-numbers`).

## Silent failures to look for

Finite-but-wrong (a CFL-violating run returns 2.4e62 with every sample finite); NaN laundering (one NaN
spread through a median and zeroed by a guard); an out-of-grid index that is a valid flat index of the next
row; `None` from `autograd.Function.backward` read as zero gradient; `autograd.functional.jvp/hvp` returning
a silent zero on a non-differentiable backward; a deprecated config key read by nothing; pocketfft not
bitwise across batch shapes; NNPACK speed cliff at batch >= 16 for float32 CPU conv.
