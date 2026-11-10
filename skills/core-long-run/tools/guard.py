#!/usr/bin/env python3
# Provenance: copied verbatim from mfold/scripts/guard.py on 2026-11-09 (MIT, Benz Poobua). Self-contained; macOS sensors.
"""
:module: guard
:author: Benz Poobua
:email: spoobua@stanford.edu
:org: Stanford Geophysics / SEP
:license: MIT
:purpose: Pause a long sweep when this laptop is too hot or draining too hard,
          and resume it when it recovers.  CLAUDE.md sect.6 describes this guard;
          until now it was run by hand.

Why it exists (CLAUDE.md traps t, ae, af).  This machine ships a **35 W adapter**
and an M4 Pro that pulls 60--80 W under load, so a sweep wide enough to matter
runs partly off the battery.  Two earlier sessions lost hours to the same class of
problem from the other side -- Low Power Mode and clamshell sleep starving a run
so badly that a healthy job looked like a slow one.  This guard makes the trade
explicit: it lets a run use more workers than the adapter can feed, and stops it
before the battery does.

What it does.  Every ``--interval`` seconds it reads the die temperature, the
thermal pressure and the battery, and

* **SIGSTOP**s every process in the target process group when the machine is above
  ``--max-temp``, at thermal pressure other than ``Nominal``, or when the battery
  has fallen to ``--min-batt``;
* **SIGCONT**s them once the temperature has fallen ``--hysteresis`` below the
  limit and the other two conditions have cleared.

SIGSTOP loses nothing: the workers are frozen, not killed, and every sweep here is
additionally resumable through ``_common.resumable_map``.

Reading the sensors needs no root.  ``pmset -g therm`` reports the thermal
pressure, and ``ioreg -rn AppleSmartBattery`` reports charge, ``SystemPowerIn`` and
a signed ``InstantAmperage`` (printed UNSIGNED when negative, hence the wrap fix
below).  **The die temperature needs a helper that is not installed here**
(``osx-cpu-temp``; ``powermetrics`` wants a password), so on this machine
:func:`die_temperature` returns ``None`` and the guard runs on thermal pressure and
the battery alone.  That is the honest configuration rather than a degraded one:
the ledger measured 73 C at SIX workers (29.3), so heat is not this laptop's limit
-- the 35 W adapter is.

:run: ``python3 scripts/guard.py --pgid <pgid>`` beside the sweep, or
      ``python3 scripts/guard.py --watch <pattern>`` to find it by command line.
"""
from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import time

# ===========================================================================
# 1. Sensors
# ===========================================================================
_AMP_WRAP = 1 << 64          # InstantAmperage is printed unsigned when negative


def thermal_pressure() -> str:
    """:return: ``Nominal``, ``Moderate``, ``Heavy``, ``Trapping``, ``Sleeping``
        or ``Unknown`` when ``pmset`` says nothing."""
    try:
        out = subprocess.run(["pmset", "-g", "therm"], capture_output=True,
                             text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return "Unknown"
    m = re.search(r"pressure level\s*=\s*(\w+)", out, re.I)
    if m:
        return m.group(1)
    # This machine prints "No thermal warning level has been recorded" while
    # nothing has fired, which is Nominal and not Unknown.  Measured 2026-09-22.
    if re.search(r"No thermal warning level has been recorded", out):
        return "Nominal"
    return "Unknown"


def battery() -> dict:
    """:return: dict with ``percent``, ``amperage_mA`` (negative = discharging),
        ``power_in_mW`` and ``external`` (on AC)."""
    try:
        out = subprocess.run(["ioreg", "-rn", "AppleSmartBattery"],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return {}

    def num(key: str) -> float | None:
        m = re.search(rf'"{key}"\s*=\s*(-?\d+)', out)
        return float(m.group(1)) if m else None

    amp = num("InstantAmperage")
    if amp is not None and amp > _AMP_WRAP / 2:      # unsigned print of a negative
        amp -= _AMP_WRAP
    ext = re.search(r'"ExternalConnected"\s*=\s*(Yes|No)', out)
    return {"percent": num("CurrentCapacity"), "amperage_mA": amp,
            "power_in_mW": num("SystemPowerIn"),
            "external": (ext.group(1) == "Yes") if ext else None}


def die_temperature() -> float | None:
    """Die temperature in degrees C from ``osx-cpu-temp``, or ``None``.

    ``powermetrics`` needs a password, so the only password-free reader is a
    helper binary, and it is NOT installed here -- this returns ``None`` on this
    machine.  That is not fatal: the guard falls back on thermal pressure and the
    battery, and heat is not this laptop's limit anyway (73 C at six workers,
    ledger 29.3).
    """
    try:
        out = subprocess.run(["osx-cpu-temp"], capture_output=True, text=True,
                             timeout=5).stdout
        m = re.search(r"([\d.]+)", out)
        if m:
            return float(m.group(1))
    except (OSError, subprocess.SubprocessError):
        pass
    return None


# ===========================================================================
# 2. The decision
# ===========================================================================
def should_pause(temp: float | None, pressure: str, batt: dict, *,
                 max_temp: float, min_batt: float) -> str | None:
    """:return: The reason to pause, or ``None`` to run."""
    if temp is not None and temp >= max_temp:
        return f"die {temp:.0f} C >= {max_temp:.0f} C"
    if pressure not in ("Nominal", "Unknown"):
        return f"thermal pressure {pressure}"
    pct = batt.get("percent")
    if pct is not None and pct <= min_batt and not batt.get("external", True):
        return f"battery {pct:.0f} % on battery power"
    if pct is not None and pct <= min_batt:
        return f"battery {pct:.0f} % <= {min_batt:.0f} %"
    return None


def should_resume(temp: float | None, pressure: str, batt: dict, *,
                  max_temp: float, min_batt: float, hysteresis: float) -> bool:
    """Resume only once every condition has cleared with margin."""
    if temp is not None and temp > max_temp - hysteresis:
        return False
    if pressure not in ("Nominal", "Unknown"):
        return False
    pct = batt.get("percent")
    return not (pct is not None and pct <= min_batt + 5.0)


# ===========================================================================
# 3. The loop
# ===========================================================================
def ensure_not_in_group(pgid: int) -> bool:
    """
    Leave ``pgid`` if we are in it, so a SIGSTOP to that group cannot freeze this guard.

    **This is the defect that froze `exp27` for 13 hours** (ledger 36.3, CLAUDE.md trap ag).
    The guard is normally launched from the same shell as the sweep, so it INHERITS the
    sweep's process group; ``os.killpg(pgid, SIGSTOP)`` then stops the guard itself, before
    the line that logs the pause, and nothing is left alive to send ``SIGCONT``.  The job
    sits frozen, at full memory, with a guard log that ends at its own startup line -- which
    is indistinguishable from "still running" unless the process STATE is checked.

    :param pgid: the process group the guard intends to signal.
    :return: True when the guard is outside ``pgid`` (already, or after detaching).
    """
    if os.getpgid(0) != pgid:
        return True
    try:
        os.setpgid(0, 0)                   # our own group, with us as leader
    except OSError:
        return False
    return os.getpgid(0) != pgid


def resources(pgid: int) -> str:
    """CPU %, resident memory of the watched group, system load and the CPU speed limit (no root needed)."""
    try:
        out = subprocess.run(["ps", "-g", str(pgid), "-o", "%cpu=,rss="], capture_output=True, text=True,
                             timeout=10).stdout.split()
        cpu = sum(float(x) for x in out[0::2])
        rss = sum(float(x) for x in out[1::2]) / 1048576.0
        load = os.getloadavg()[0]
        therm = subprocess.run(["pmset", "-g", "therm"], capture_output=True, text=True, timeout=10).stdout
        lim = [ln.split("=")[-1].strip() for ln in therm.splitlines() if "CPU_Speed_Limit" in ln]
        return f"job cpu {cpu:.0f} %, rss {rss:.1f} GB, load {load:.1f}, speed limit {lim[0] + ' %' if lim else 'none'}"
    except (OSError, subprocess.SubprocessError, ValueError):
        return "resources n/a"


def find_pgid(pattern: str) -> int | None:
    """Process group of the newest process whose command line matches."""
    try:
        out = subprocess.run(["ps", "-eo", "pgid,command"], capture_output=True,
                             text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    hits = [int(ln.split(None, 1)[0]) for ln in out.splitlines()[1:]
            if pattern in ln and "guard.py" not in ln]
    return hits[-1] if hits else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pgid", type=int, default=None)
    ap.add_argument("--watch", type=str, default=None,
                    help="substring of the sweep's command line")
    ap.add_argument("--interval", type=float, default=20.0)
    ap.add_argument("--max-temp", type=float, default=95.0)
    ap.add_argument("--min-batt", type=float, default=50.0)
    ap.add_argument("--hysteresis", type=float, default=8.0)
    ap.add_argument("--duty", type=str, default="",
                    help="ON,OFF minutes: after ON minutes running, pause OFF minutes to cool (2026-11-09)")
    ap.add_argument("--beat", type=float, default=900.0, help="seconds between heartbeat/resource lines")
    a = ap.parse_args()
    duty_on, duty_off = (float(x) * 60.0 for x in a.duty.split(",")) if a.duty else (0.0, 0.0)

    pgid = a.pgid or (find_pgid(a.watch) if a.watch else None)
    if pgid is None:
        print("guard: nothing to watch", file=sys.stderr)
        return 2

    if not ensure_not_in_group(pgid):
        print(f"guard: REFUSING to watch its own process group {pgid} -- a SIGSTOP would "
              f"freeze this guard too and nothing would ever resume the job", file=sys.stderr)
        return 2
    print(f"guard: watching pgid {pgid}  (max {a.max_temp:.0f} C, "
          f"min battery {a.min_batt:.0f} %, every {a.interval:.0f} s)", flush=True)

    paused = False
    resting_until = 0.0                  # duty-cycle rest (cooling), separate from a sensor pause
    run_since = time.time()
    last_beat = -1
    while True:
        try:
            os.killpg(pgid, 0)
        except (ProcessLookupError, PermissionError):
            print("guard: target gone; exiting", flush=True)
            return 0
        temp, pressure, batt = die_temperature(), thermal_pressure(), battery()
        now = time.time()
        if duty_on > 0 and not paused:
            if resting_until == 0.0 and now - run_since >= duty_on:
                print(f"guard: RESTING {duty_off / 60:.0f} min (duty cycle)", flush=True)
                os.killpg(pgid, signal.SIGSTOP)
                resting_until = now + duty_off
            elif resting_until and now >= resting_until:
                os.killpg(pgid, signal.SIGCONT)
                resting_until, run_since = 0.0, now
                print("guard: rest over, resumed", flush=True)
        if resting_until:
            time.sleep(a.interval)
            continue
        if not paused:
            why = should_pause(temp, pressure, batt,
                               max_temp=a.max_temp, min_batt=a.min_batt)
            if why:
                # Log BEFORE signalling.  If the SIGSTOP ever reaches this process the
                # message is already on disk, which is what turned a 13 h freeze into a
                # silent one the first time.
                print(f"guard: PAUSED -- {why}", flush=True)
                os.killpg(pgid, signal.SIGSTOP)
                paused = True
        elif should_resume(temp, pressure, batt, max_temp=a.max_temp,
                           min_batt=a.min_batt, hysteresis=a.hysteresis):
            os.killpg(pgid, signal.SIGCONT)
            paused = False
            print("guard: resumed", flush=True)
        if int(time.time() // a.beat) != last_beat:
            last_beat = int(time.time() // a.beat)
            pct = batt.get("percent")
            print(f"guard: alive, {'PAUSED' if paused else 'running'}, battery "
                  f"{pct if pct is not None else '?'} %, pressure {pressure}; {resources(pgid)}", flush=True)
        time.sleep(a.interval)


if __name__ == "__main__":
    raise SystemExit(main())
