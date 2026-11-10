"""
:module: src/<name>.py
:auth: Benz Poobua
:email: spoobua (at) stanford.edu
:org: Stanford University
:license: MIT
:purpose: One line: what this module computes.
:reference: Papers it implements, with years and equation numbers (e.g. Zhang (2026) DSP 168:105509, eqs. 7-12).
:provenance: (only for extracted code) origin repo URL @ commit, original path, authors, licence, what changed.

Description:
What it does and why, in prose. Long docstrings carry THEORY (the derivation, the conventions, the
regime where the method pays), not just parameter lists -- see das_ani/src/ani.py::choose_block_size_bw.

Key Features:
    - bullets that name the actual design decisions (e.g. "float64 accumulator, float32 storage")
"""
from __future__ import annotations

import numpy as np

# ===========================================================================
# 1. <First section: e.g. Configuration helpers>
# ===========================================================================


def example(x: np.ndarray, fs: float, *, axis: int = -1) -> np.ndarray:
    """
    One-line summary.

    Longer explanation with the math the function implements, in the repo's sign/lag convention.

    :param x: Input array, (nch, nt) float32, channel-major.
    :param fs: Processing sampling rate in Hz (fs_proc, never the raw rate downstream of ingest).
    :param axis: Axis along which to operate.
    :return: Output array, same shape and dtype as ``x``.
    :raises ValueError: If ``x`` contains non-finite values.
    """
    if not np.all(np.isfinite(x)):
        raise ValueError("example: non-finite input")
    return x


# ===========================================================================
# 2. <Next section>
# ===========================================================================
