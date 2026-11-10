---
name: code-hpc
description: Running on Stanford's Sherlock cluster with SLURM the das_ani way - preflight submit.sh, module setup script, safe sbatch headers, Python-side thread control, GPU type constraints, TF32 pinned off, sync/fetch without data loss, requeue-safe resume. Use when writing or editing slurm/ scripts, submit.sh, sherlock_setup.sh, Makefile sync/fetch targets, or planning a cluster run.
---

# code-hpc

Reference implementation: `das_ani/` (`submit.sh`, `sherlock_setup.sh`, `slurm/*.slurm`, Makefile
`sync reachable fetch fetch-logs slurm-prep data-plan`). The older notes in
`../../../SHERLOCK_old_need_revise.md` are pending revision (root TASKS.md); prefer das_ani's files.

## sbatch script rules

- `#!/bin/bash` + `set -euo pipefail` (otherwise a failed stage is followed by a stage that "succeeds" on
  partial output and the job exits 0).
- `cd "${SLURM_SUBMIT_DIR}"` — never a hard-coded checkout path.
- `mkdir -p logs results` before anything; `--output=logs/%x_%j.out` AND `--error=logs/%x_%j.err`
  (SLURM does not create the log directory; a missing one kills the job with no log).
- Config path from the environment with a default: `CC_CFG="${CC_CFG:-configs/urban_cc.yaml}"`.
- Threads are set **in Python** from `SLURM_CPUS_PER_TASK` (das_ani `cc._set_thread_env`); do not export
  `OMP_NUM_THREADS` in the script — it gets overridden or oversubscribes.
- GPU jobs: request the type with `--constraint` (the `gpu` partition mixes V100 / RTX 3090 / L40S / H100;
  Pascal and V100 lack bf16/TF32), give the CPU side enough cores, stop at once when CUDA is absent, and
  pin TF32 off in code (`torch.backends.cuda.matmul.allow_tf32 = False`,
  `torch.backends.cudnn.allow_tf32 = False`); record the executed precision in the run manifest.

## Submit and transfer

- `bash submit.sh [cpu|gpu|eval] [--check|--estimate]`: preflight (config exists, logs dir, modules import,
  data_root holds inputs, compiled wheels built on the login node) before `sbatch`; `--estimate` asks
  `sbatch --test-only` when each option would start.
- `make sync` pushes code with `--delete` but **excludes** `data/ results/ logs/` and the venv; `make fetch`
  pulls products **without** `--delete` and excludes raw archives; `make reachable` checks ssh first.
- Results must be resumable and requeue-idempotent (fingerprinted resume state, skip-and-log) — the same rules
  as `benz:core-long-run`.

## Facts to carry

- Bitwise identity is a property of a build: anchors made on the laptop (arm64, torch X) may differ in the
  last bit on the cluster (x86-64, torch Y). Gate cross-machine comparisons with a calibrated tolerance.
- Benchmarks are multi-tenant: report ratios at matched parameters, 4 runs, discard warm-up, median of 3.
- Nothing about the cluster is "verified" until it ran there: say "not run on Sherlock" otherwise.
