---
name: core-long-run
description: Turn any job longer than ~10 minutes (sweeps, campaigns, inversions, notebook batches, big downloads) into a resumable, trackable, guarded offline script that Benz launches himself. Use before starting a long computation, when a run may outlive the session or the Claude account, and when choosing worker counts on the laptop.
---

# core-long-run

A long run belongs in a script Benz can launch, watch and resume without Claude — he switches Claude
accounts, and sessions end. **Always ask before launching** anything long; hand over the command instead
of running it unless he says "run it".

## Steps

1. **Preflight one task** in a fresh process: wall time, peak memory (`/usr/bin/time -l`, or
   `ru_maxrss`), threads it really uses. Completion: you can state "one task = X s, Y GiB".
2. **Size the run** from that measurement: `workers = min(cores // threads_per_worker,
   floor(free_mem / private_per_task))`, then **cap at what the power adapter feeds** (this laptop:
   2 workers on the 35 W adapter, 4 on 70 W; mfold trap af). Estimate total time = tasks x task_time /
   workers x 1.3. Check `df -h` for output space (disk was 96 % full on 2026-11-09).
3. **Make it resumable before it is fast.** Each task has a key; results are written atomically
   (write to `*.tmp`, `os.replace`) and appended to a partial log the moment they land; a rerun skips keys
   whose output exists **and** is complete; a run under a different configuration is refused, never merged
   (config fingerprint). Patterns to copy: `mfold/scripts/_common.py::resumable_map`,
   `das_ani/src/cc.py` (fingerprinted resume state, skip-and-log), `sigGP/src/workflow.py` (campaign runner).
4. **Make it trackable.** Unbuffered log (`python -u`) to `logs/<name>_<YYYYmmdd_HHMMSS>.log`; a
   `progress.json` (done / total / failed / ETA); a one-line status command; per-stage timings in the final
   report; failures recorded per task, never fatal to the campaign.
5. **Guard the machine.** `caffeinate -dimsu` around the job; lid open (clamshell sleep stops it even with
   `caffeinate -i`); `pmset -g | grep powermode` must be 0 (Low Power Mode starves runs); one heavy sweep at
   a time; run `tools/guard.py --watch <pattern>` beside it (pauses with SIGSTOP on thermal pressure or
   low battery, resumes on recovery; it refuses to watch its own process group). Thread variables
   (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `RAYON_NUM_THREADS`) are set in Python before imports start pools.
6. **Write the script from `templates/run_offline.sh`** and `bash -n` it. Completion: the script runs
   from any shell with no Claude involvement, and a second launch after a kill resumes.
7. **Hand over** using the block below, then stop and wait for Benz.

## Hand-over block (paste into chat and into TASKS.md)

```
RUN:      bash <repo>/scripts/run_<name>.sh            (from: <cwd>)
WHAT:     <tasks, data, config>                    ESTIMATE: <h> on <workers> workers (<one task = X s, Y GiB>)
WATCH:    tail -f <log>   |  cat <progress.json>   |  ps -o pid,stat,time,command -g <pgid>
RESUME:   rerun the same command (finished keys are skipped)
STOP:     kill -TERM -<pgid>   (then check for PPID-1 orphans: ps -ef | grep <script>)
OUTPUT:   <dir>     NEXT SESSION: read <progress.json>, then <what to check>
```

## Traps already paid for

- A stalled job is diagnosed by process STATE and CPU time (`ps -o stat,time`), never by log silence or
  wall clock; some sweeps print only at the end.
- `pkill -f <script>` misses spawned workers re-parented to PID 1: kill orphans by PID.
- Peak memory needs one fresh process per configuration (`ru_maxrss` never falls); macOS keeps freed large
  blocks resident (`MallocLargeCache`), so Mac numbers overstate Linux.
- rayon pools do not survive `fork`: use `multiprocessing.get_context("spawn")` (callers need a
  `__main__` guard).
- A float64 CPU `conv1d` with a long kernel can unfold the whole batch (~54 GB, invisible to `ps`): chunk it.
- On the cluster, use SLURM instead (`benz:code-hpc`): same resume rules, `set -euo pipefail`, logs dir first.
