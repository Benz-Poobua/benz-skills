#!/usr/bin/env python3
"""
:module: skills/paper-bib/scripts/find_dup_pdfs.py
:auth: Benz Poobua (written with Claude, 2026-11-09)
:license: MIT
:purpose: Find duplicate or colliding PDFs before adding a paper: identical content (md5), the same
          normalized stem, or the same first-author + year with a different suffix. Read-only.

Usage:
    python3 find_dup_pdfs.py [NEW.pdf ...] --roots DIR [DIR ...]
    (no NEW.pdf: report every duplicate/collision inside the roots)

Default roots: mypaper/mybible/{alg,etc,fwi,das,cs} and inspiring_papers under the Imaging_Project root.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PROJECT = Path("/Users/spoobua/Desktop/Imaging_Project")
DEFAULT_ROOTS = [PROJECT / "mypaper/mybible" / d for d in ("alg", "etc", "fwi", "das", "cs")] + [PROJECT / "inspiring_papers"]


def md5(path: Path) -> str:
    """:return: hex md5 of the file content."""
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_stem(stem: str) -> str:
    """:return: lower-case ASCII stem without separators (Klöwer_etal_2021 -> klowerEtal2021 -> 'kloweretal2021')."""
    s = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def author_year(stem: str) -> str | None:
    """:return: 'firstauthor_YYYY' (suffix letters and topic tags dropped), or None when no year."""
    m = re.match(r"^(.+?)_(?:etal_)?(\d{4})[a-z]?(?:_.*)?$", stem)
    if not m:
        return None
    first = m.group(1).split("_")[0]
    return f"{norm_stem(first)}_{m.group(2)}"


def scan(roots: list[Path]) -> list[Path]:
    """:return: every PDF under the roots (recursively)."""
    out: list[Path] = []
    for r in roots:
        if r.is_dir():
            out += [p for p in r.rglob("*.pdf") if p.is_file()]
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("new", nargs="*", type=Path)
    ap.add_argument("--roots", nargs="*", type=Path, default=DEFAULT_ROOTS)
    a = ap.parse_args(argv)
    lib = scan(a.roots)
    by_hash: dict[str, list[Path]] = defaultdict(list)
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_ay: dict[str, list[Path]] = defaultdict(list)
    for p in lib:
        by_stem[norm_stem(p.stem)].append(p)
        ay = author_year(p.stem)
        if ay:
            by_ay[ay].append(p)
    targets = a.new or lib
    if a.new or True:
        for p in lib:
            by_hash[md5(p)].append(p)
    found = 0
    seen: set[tuple[str, ...]] = set()

    def report(kind: str, group: list[Path]) -> None:
        nonlocal found
        key = (kind,) + tuple(sorted(map(str, group)))
        if len(group) > 1 and key not in seen:
            seen.add(key)
            found += 1
            print(f"[{kind}]")
            for g in sorted(group):
                print(f"   {g}")

    for p in targets:
        h = md5(p) if p.exists() else None
        report("same content", sorted(set(by_hash.get(h, []) + ([p] if a.new else []))) if h else [])
        report("same stem", sorted(set(by_stem.get(norm_stem(p.stem), []) + ([p] if a.new else []))))
        ay = author_year(p.stem)
        if ay:
            report("same first author + year (check suffixes)", sorted(set(by_ay.get(ay, []) + ([p] if a.new else []))))
    print(f"scanned {len(lib)} PDFs; {found} group(s) to check")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
