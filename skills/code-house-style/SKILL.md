---
name: code-house-style
description: The ecosystem's coding standard, taken from das_ani (the reference repo) - flat src/ package, reST module headers, load_config/get_cfg, one rcParams block, CUDA-or-CPU, fingerprinted resumable runs, config-driven CLIs, SLURM, generated notebooks, provenance headers. Use when creating a repo or module, writing plots, configs, CLIs or Makefiles, or when two repos disagree on style.
---

# code-house-style

**`das_ani` is the reference.** Its `CLAUDE.md` sect. 5 is normative; where repos disagree, das_ani wins.
This skill is the portable summary plus copy-ready files in `references/`.

## Layout (das_ani CLAUDE.md sect. 5.1)

```
<repo>/
  CLAUDE.md  TASKS.md  LEDGER.md  README.md   rules / next / record / exhaustive user doc
  pyproject.toml   packages = ["src"]  (NOT package-dir={"":"src"}: that breaks `python -m src.cc`)
  Makefile         help test lint ci nb clean slurm-prep sync reachable fetch fetch-logs (+ repo verbs)
  src/             flat package imported as src.*: utils.py (I/O, config) ... plots.py (every figure)
  configs/*.yaml   scripts/ (build_*_nb.py generators, benchmarks)   tests/   notebooks/   slurm/
  submit.sh  sherlock_setup.sh          cluster preflight + module env (benz:code-hpc)
  data/ results/ logs/                  gitignored outputs;  <repo>_env/  the venv (gitignored)
```

## Code

- **Module header**: reST docstring `:module: :auth: :email: :org: :license: :purpose: :reference:`
  (+ `:provenance:` for extracted code), then `from __future__ import annotations`; full type hints;
  numbered `# ===` section dividers; `:param:` / `:return:` / `:raises:` on every public function; long
  docstrings carry the theory. Template: `references/module_header.py`.
- **Config**: `load_config` + `get_cfg(cfg, ["a","b"], default, required=)` copied **verbatim**
  (`references/utils_config.py`). A YAML `null` returns `None`, not the default: write `get_cfg(...) or fallback`.
  Deprecated keys are accepted with a logged warning, never silently (das_ani `cc._get_bw_cfg`).
- **Arrays and units**: DAS data `(nch, nt)` float32 channel-major; models `(nz, nx)`, z down, metres, m/s;
  downstream of ingest pass `fs_proc`, never the raw rate. deepwave locations: LONG `(n_shots, n, 2)` `[iz, ix]`.
- **Devices**: CUDA or CPU only — **MPS is banned** (no float64, no deepwave backends). One `pick_device()`
  per repo. On CUDA pin TF32 off (`torch.backends.cuda.matmul.allow_tf32 = False`,
  `torch.backends.cudnn.allow_tf32 = False`) and record the executed precision.
- **Numerics**: float64 accumulators for long sums stored in float32 (das_ani `stack._streaming_mean`);
  reject non-finite input instead of laundering it; a knob whose executed value differs from the requested
  one must raise or warn.
- **Adjoints**: autograd supplies them; a hand-written adjoint is a claim carried by dot-product and
  finite-difference gates (`benz:code-verify`).

## Plots (das_ani sect. 5.6)

`src/plots.py` owns every figure; the one rcParams block is `references/plots_rcparams.py`
(das_ani's block + `pdf.fonttype 42`); `layout="constrained"`; one `_save()` helper; `title_pad`
arguments; axes labelled with units. Notebooks paste the same block in their first cell. Book figures
use the book's block (`mypaper/mybible/skills/book-figures`).

## Runs

- CLIs are config-driven: `python -m src.<stage> --config configs/<run>.yaml --verbose`.
- **Resumable and honest**: a resume state records a fingerprint of the values the products depend on;
  another configuration refuses (`ConfigMismatchError`) instead of mixing; a task is skipped only when it is
  listed AND its output is complete; a failing input is skipped-and-logged (`skipped_files.jsonl`), never
  fatal to the campaign. (das_ani `src/cc.py`, sect. 2k of its LEDGER.)
- Worker pools are `spawn`ed; thread budgets are set in Python from `SLURM_CPUS_PER_TASK`, never by
  exporting `OMP_NUM_THREADS` in a batch script.
- **File-name grammar is load-bearing** (das_ani `<basename>_cc_<vs:03d>_<method>.npy`): reuse it so
  products drop into existing tools.

## Notebooks, tests, docs

Generated notebooks with print + assert per claim (`benz:code-notebooks`); `pytest` is the first command
in every repo; ruff clean (`make lint`); `README.md` is exhaustive for users; `CITATIONS.md` /
`docs/EXTRACTION_MAP.md` record every extraction (`benz:code-extract`).
