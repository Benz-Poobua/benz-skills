#!/usr/bin/env python3
"""
:module: skills/paper-bib/scripts/ris2bib.py
:auth: Benz Poobua (written with Claude, 2026-11-09)
:license: MIT
:purpose: Convert a publisher RIS export to a BibTeX entry keyed by the Lastname_etal_YYYY convention.

Usage:
    python3 ris2bib.py <file.ris> [--key KEY] [--ascii]

The output is a DRAFT: verify every field against the PDF's first page and the DOI before use
(benz:paper-bib). Fields missing from the RIS are left out, never guessed. `--ascii` converts common
accented letters to LaTeX escapes (mybible's bibs are ASCII-only).
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

TYPE_MAP = {"JOUR": "article", "JFULL": "article", "EJOUR": "article", "BOOK": "book", "EBOOK": "book",
            "CHAP": "incollection", "ECHAP": "incollection", "CONF": "inproceedings", "CPAPER": "inproceedings",
            "THES": "phdthesis", "RPRT": "techreport", "GEN": "misc", "ELEC": "misc", "DATA": "misc", "COMP": "misc"}
ESCAPES = {"á": "{\\'a}", "é": "{\\'e}", "í": "{\\'i}", "ó": "{\\'o}", "ú": "{\\'u}", "ý": "{\\'y}",
           "à": "{\\`a}", "è": "{\\`e}", "ä": '{\\"a}', "ë": '{\\"e}', "ï": '{\\"i}', "ö": '{\\"o}', "ü": '{\\"u}',
           "â": "{\\^a}", "ê": "{\\^e}", "ô": "{\\^o}", "ç": "{\\c{c}}", "ñ": "{\\~n}", "ã": "{\\~a}",
           "š": "{\\v{s}}", "č": "{\\v{c}}", "ř": "{\\v{r}}", "ž": "{\\v{z}}", "ň": "{\\v{n}}", "ě": "{\\v{e}}",
           "å": "{\\aa}", "ø": "{\\o}", "ß": "{\\ss}", "ł": "{\\l}", "–": "--", "—": "---"}


def parse_ris(text: str) -> list[dict[str, list[str]]]:
    """:return: one dict per record mapping RIS tags to their values (in order)."""
    recs: list[dict[str, list[str]]] = []
    cur: dict[str, list[str]] = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  - ?(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            if cur:
                recs.append(cur)
            cur = {}
            continue
        cur.setdefault(tag, []).append(val)
    if cur:
        recs.append(cur)
    return recs


def surname(author: str) -> str:
    """:return: the family name of 'Last, First' or 'First Last'."""
    author = author.strip()
    last = author.split(",")[0] if "," in author else author.split()[-1]
    return last.strip()


def key_for(authors: list[str], year: str) -> str:
    """:return: Lastname_YYYY / Lastname_Lastname_YYYY / Lastname_etal_YYYY (ASCII, spaces -> _)."""
    def clean(s: str) -> str:
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
        return re.sub(r"[^A-Za-z\-]+", "_", s).strip("_")
    names = [clean(surname(a)) for a in authors] or ["Anon"]
    if len(names) == 1:
        stem = names[0]
    elif len(names) == 2:
        stem = f"{names[0]}_{names[1]}"
    else:
        stem = f"{names[0]}_etal"
    return f"{stem}_{year or 'XXXX'}"


def to_ascii(s: str) -> str:
    """:return: ``s`` with known accented letters replaced by LaTeX escapes."""
    return "".join(ESCAPES.get(c, ESCAPES.get(c.lower(), c)) for c in s)


def to_bibtex(rec: dict[str, list[str]], key: str | None, ascii_only: bool) -> str:
    """:return: one BibTeX entry string (draft)."""
    get = lambda *tags: next((rec[t][0] for t in tags if t in rec and rec[t]), "")  # noqa: E731
    authors = rec.get("AU", []) + rec.get("A1", [])
    year = re.sub(r"\D.*", "", get("PY", "Y1", "DA"))[:4]
    etype = TYPE_MAP.get(get("TY"), "misc")
    fields: list[tuple[str, str]] = []
    if authors:
        fields.append(("author", " and ".join(a.strip() for a in authors)))
    title = get("TI", "T1")
    if title:
        fields.append(("title", "{" + title + "}"))
    journal = get("JO", "JF", "T2", "JA")
    if etype == "article" and journal:
        fields.append(("journal", journal))
    elif etype in ("incollection", "inproceedings") and get("T2", "BT"):
        fields.append(("booktitle", get("T2", "BT")))
    for tag, name in (("VL", "volume"), ("IS", "number"), ("PB", "publisher"), ("DO", "doi"), ("SN", "issn"),
                      ("UR", "url")):
        if get(tag):
            fields.append((name, get(tag)))
    sp, ep = get("SP"), get("EP")
    if sp:
        fields.append(("pages", f"{sp}--{ep}" if ep and ep != sp else sp))
    if year:
        fields.append(("year", year))
    k = key or key_for(authors, year)
    body = ",\n".join(f"  {n} = {{{to_ascii(v) if ascii_only else v}}}" for n, v in fields)
    return f"@{etype}{{{k},\n{body}\n}}\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ris", type=Path)
    ap.add_argument("--key", default=None, help="override the key (only for a single-record file)")
    ap.add_argument("--ascii", action="store_true", help="LaTeX-escape accented letters")
    a = ap.parse_args(argv)
    recs = parse_ris(a.ris.read_text(errors="ignore"))
    if not recs:
        print("no RIS records found", file=sys.stderr)
        return 1
    if a.key and len(recs) > 1:
        print("--key needs a single-record file", file=sys.stderr)
        return 2
    for r in recs:
        sys.stdout.write(to_bibtex(r, a.key, a.ascii) + "\n")
    print(f"% {len(recs)} draft entr{'y' if len(recs) == 1 else 'ies'}: VERIFY every field against the PDF and DOI",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
