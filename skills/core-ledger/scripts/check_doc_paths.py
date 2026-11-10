#!/usr/bin/env python3
"""
:module: skills/core-ledger/scripts/check_doc_paths.py
:auth: Benz Poobua (written with Claude, 2026-11-09)
:license: MIT
:purpose: Report backticked paths in a markdown doc (CLAUDE.md, TASKS.md, PATHS.md) that do not exist.

Usage:
    python3 check_doc_paths.py <doc.md> [<doc.md> ...]

A path is any `backticked` token that contains a '/' or ends in a known file suffix, with no spaces,
no glob/brace characters and no placeholders (<...>). It is resolved relative to the doc's directory.
Exit status 1 when anything is missing, so the check can gate an edit. Read-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SUFFIXES = (".md", ".py", ".sh", ".tex", ".bib", ".yaml", ".yml", ".json", ".toml", ".ipynb",
            ".slurm", ".rs", ".jl", ".txt", ".pdf", ".npz", ".cfg")
TOKEN = re.compile(r"`([^`\s]+)`")
SKIP_CHARS = set("*{}<>$|()=,;'\"")


PLACEHOLDER = re.compile(r"(NN|YYYY|MMDD|HHMMSS|XXX|<|>)")


def candidate(tok: str) -> bool:
    """:return: True when the token looks like a filesystem path worth checking.

    Only tokens with a '/' are checked (a bare ``guard.py`` is ambiguous); placeholders (NN, YYYY),
    globs, URLs, ``module::symbol`` and ``name:version`` forms are skipped.
    """
    if any(c in SKIP_CHARS for c in tok) or tok.startswith(("http", "-", "~", "@", "#")):
        return False
    if "::" in tok or tok.endswith(":") or PLACEHOLDER.search(tok):
        return False
    if "/" not in tok:
        return False
    first = tok.split("/")[0]
    if "." in first and not first.startswith(".") and not first.endswith(SUFFIXES):
        return False                                   # dotted module path such as autograd.functional.hvp/jvp
    # a path starts with ./, ../, a dotted dir, or a word segment; skip math like J/J0 (no suffix, no dir hint)
    return tok.startswith((".", "/")) or tok.endswith(SUFFIXES) or tok.endswith("/") or first.islower() or "_" in first


def check(doc: Path) -> list[str]:
    """:return: missing paths referenced by ``doc`` (relative to its directory)."""
    base = doc.parent
    missing: list[str] = []
    for lineno, line in enumerate(doc.read_text(errors="ignore").splitlines(), 1):
        for tok in TOKEN.findall(line):
            if not candidate(tok):
                continue
            p = tok.split(":")[0].rstrip(".")          # drop :line suffixes and trailing dots
            if not (base / p).exists() and not Path(p).exists():
                missing.append(f"{doc}:{lineno}: {tok}")
    return missing


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    missing = [m for a in argv for m in check(Path(a))]
    for m in missing:
        print("MISSING", m)
    print(f"checked {len(argv)} file(s); missing {len(missing)}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
