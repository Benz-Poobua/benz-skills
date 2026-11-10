#!/usr/bin/env bash
# run_offline.sh — template for a long, resumable, guarded run on Benz's Mac.
# Copy to <repo>/scripts/run_<name>.sh, fill the CONFIG block, `bash -n` it, hand the command to Benz.
# Launch:  bash scripts/run_<name>.sh            Resume: run the same command again.
# Stop:    kill -TERM -<pgid printed at start>    Watch: tail -f <log>  /  cat <progress json>
set -euo pipefail

# ----------------------------------------------------------------------------- CONFIG (edit)
NAME="sweep_name"                                   # used for log/progress names
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${REPO}/<repo>_env/bin/python"                  # the repo's venv python
CMD=("$PY" -u -m scripts.my_sweep --config configs/my_sweep.yaml --workers 2 --resume)
WORKERS_MAX=2                                       # 35 W adapter: 2; 70 W: 4 (mfold trap af)
MIN_FREE_GB=20                                      # refuse to start below this much free disk
THREADS_PER_WORKER=1
GUARD="${HOME}/Desktop/Imaging_Project/benz-skills/skills/core-long-run/tools/guard.py"

# ----------------------------------------------------------------------------- PREFLIGHT
cd "$REPO"
mkdir -p logs results
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="logs/${NAME}_${STAMP}.log"
[ -x "$PY" ] || { echo "no python at $PY"; exit 1; }
free_gb=$(df -g . | awk 'NR==2{print $4}')
[ "${free_gb:-0}" -ge "$MIN_FREE_GB" ] || { echo "only ${free_gb} GB free (< ${MIN_FREE_GB}); free space first"; exit 1; }
pm=$(pmset -g 2>/dev/null | awk '/powermode|lowpowermode/{print $2; exit}')
[ "${pm:-0}" = "0" ] || echo "WARNING: Low Power Mode is on (pmset powermode=${pm}); the run will be starved"
pmset -g batt 2>/dev/null | head -2 || true
echo "lid must stay OPEN (clamshell sleep stops the run even under caffeinate)"

export OMP_NUM_THREADS="$THREADS_PER_WORKER" MKL_NUM_THREADS="$THREADS_PER_WORKER" \
       OPENBLAS_NUM_THREADS="$THREADS_PER_WORKER" RAYON_NUM_THREADS="$THREADS_PER_WORKER" \
       PYTHONDONTWRITEBYTECODE=1

# ----------------------------------------------------------------------------- LAUNCH (own process group)
echo "[$(date)] start ${NAME}: ${CMD[*]}" | tee -a "$LOG"
# caffeinate: -d display, -i idle, -m disk, -s system (AC), -u user activity
set +e
setsid caffeinate -dimsu "${CMD[@]}" >>"$LOG" 2>&1 < /dev/null &
JOB=$!
set -e
sleep 2
PGID=$(ps -o pgid= -p "$JOB" | tr -d ' ')
echo "job pid=$JOB pgid=$PGID log=$LOG" | tee -a "$LOG"

# thermal / battery guard in its OWN process group (it refuses to watch its own group)
if [ -f "$GUARD" ]; then
  setsid python3 "$GUARD" --pgid "$PGID" --interval 30 >>"logs/${NAME}_${STAMP}_guard.log" 2>&1 < /dev/null &
  echo "guard pid=$! log=logs/${NAME}_${STAMP}_guard.log"
fi

cat <<EOF
WATCH:  tail -f $LOG
STATE:  ps -o pid,stat,time,command -g $PGID
STOP:   kill -TERM -$PGID     (then: ps -ef | grep ${NAME}  for PPID-1 orphans)
RESUME: bash $0
EOF
