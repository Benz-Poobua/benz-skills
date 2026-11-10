"""
:module: references/plots_rcparams.py (benz-skills code-house-style)
:purpose: The ONE plotting style block for code repos and their notebooks.

Source: das_ani/src/plots.py lines 33-46 (the reference repo), plus the two font-embedding keys the sibling
repos added (das_3sta CLAUDE.md sect. 4: `pdf.fonttype 42`). Put this block at the top of every repo's
`src/plots.py` and in the first code cell of every notebook. Book figures (mypaper/mybible) use the book's own
block (smaller fonts for page width): see mypaper/mybible/skills/book-figures/SKILL.md.

Figure rules that go with it: `fig, ax = plt.subplots(..., layout="constrained")`; every figure saved through
one `_save(fig, path)` helper (PDF for papers, PNG 300 dpi for notebooks/README); titles take `title_pad`;
axes labelled with units ("x (m)", "z (m)", "Velocity (m/s)", "Time (s)", "Frequency (Hz)"); models shown
as (nz, nx) with z down; colormaps stated in the caption; seeds fixed.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

PARAMS: dict = {
    "savefig.dpi": 300,
    "axes.labelsize": 14,
    "axes.titlesize": 18,
    "font.size": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "text.usetex": False,
    "figure.figsize": [12, 6],
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "pdf.fonttype": 42,          # embed TrueType: editable text in Illustrator, accepted by journals
    "ps.fonttype": 42,
}
mpl.rcParams.update(PARAMS)


def _save(fig: plt.Figure, path: str | Path, *, dpi: int | None = None, close: bool = True) -> Path:
    """
    Save a figure where the caller says, creating the directory.

    :param fig: Figure to save.
    :param path: Output file (suffix decides the format: .pdf for papers, .png for notebooks/README).
    :param dpi: Override `savefig.dpi` (300) only when a target demands it.
    :param close: Close the figure after saving (avoids leaking figures in batch runs).
    :return: The resolved output path.
    """
    out = Path(path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, bbox_inches="tight")
    if close:
        plt.close(fig)
    return out
