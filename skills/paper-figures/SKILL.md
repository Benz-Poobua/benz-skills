---
name: paper-figures
description: Reproducible figures for manuscripts and books - one script per figure family regenerates the PDF from code and artifacts, deterministic seeds, the right rcParams block, captions that state what is computed and with which parameters. Use when creating or changing a figure, adding \smartfig to a book chapter, or when a figure's numbers change.
---

# paper-figures

## Rules

- **Every figure has a generator**: `scripts/fig_<name>.py` writes `fig/<name>.pdf` (book: the name matches
  `\smartfig{<name>}`); legacy figures (`fig_legacy/`) are reference only, never included.
- **Recompute, do not redraw**: the script reads the gate artifacts or calls the repo code that produced them.
  Repo physics runs in the repo's own environment by subprocess (two repos' flat `src` packages shadow each
  other in one interpreter); expensive outputs are cached with their provenance (`notes/data/`).
- **Style**: code-repo figures and notebooks use the house block (`benz:code-house-style`,
  `references/plots_rcparams.py`); book figures use the book block
  (`mypaper/mybible/skills/book-figures/SKILL.md`: smaller fonts for page width). Always `layout="constrained"`,
  `pdf.fonttype 42`, units on every axis, (nz, nx) z-down for models, seeds fixed.
- **Captions reproduce**: what is plotted, how it was computed, the parameters (frequency band, offsets,
  model, iteration), and the artifact or script; a reader must be able to regenerate it from caption + script.
- **Numbers in a figure** (annotations, legends) are traced like numbers in text (`benz:paper-numbers`).

## Steps

1. Write/modify the generator; run it from the document root; confirm only `fig/` changed.
2. Compile the document; the placeholder box disappears; check the figure at print size.
3. For the book: run `mypaper/mybible/skills/book-verify` gates; link notebooks if the figure has one.
