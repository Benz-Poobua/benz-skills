---
name: paper-bib
description: BibTeX and PDF-library hygiene - the Lastname_etal_YYYY filename and key convention, duplicate checks (hash, same stem, same author+year), every field verified against the PDF and DOI, RIS-to-BibTeX conversion, no invented fields, no ghost keys. Use when adding a paper or bib entry, importing .ris/.bib from a publisher, moving PDFs from inspiring_papers into mypaper, or before compiling a manuscript.
---

# paper-bib

## The convention (measured on mybible's 866 PDFs, 2026-11-09)

| authors | file / key | examples |
|---|---|---|
| one | `Lastname_YYYY` | `Biondi_2006` |
| two | `Lastname_Lastname_YYYY` | `Virieux_Operto_2009` |
| three or more | `Lastname_etal_YYYY` | `Kukreja_etal_2022` |
| collision | suffix `a`, `b` | `Amestoy_etal_2023a`, `Klöwer_etal_2021b` |
| rare disambiguator | `_<topic>` after the year | `Li_etal_2025_sep` |
| supplementary material | `_sup` after the year (no bib key of its own) | `Yuan_etal_2024_sup` |

The **bib key equals the PDF stem**. Particles stay as written with underscores (`van_den_Berg_...`,
`de_Ridder_...`). Prefer ASCII in new file names (existing names with accents, e.g. `Klöwer`, `Váňa`,
are kept; never rename a file other docs cite without updating them). Bibliographies: `mypaper/mybible/`
`fwi_ref.bib`, `alg_ref.bib`, `das_ref.bib`, `cs_ref.bib`, `rocks_ref.bib`; manuscripts reuse these or keep
a local bib whose keys follow the same rule.

## Steps to add a paper

1. **Duplicates first**: `python3 scripts/find_dup_pdfs.py <new.pdf> --roots <mybible dirs> <inspiring_papers>`
   reports identical hashes, the same normalized stem (case/accents/underscores ignored) and the same
   first-author + year with another suffix. Same author+year but a different paper -> assign the next suffix
   and check every existing citation of the old key still points to the right paper.
2. **Name the file** by the convention; put it in the right folder (`fwi/` FWI and imaging, `alg/` math and
   algorithms, `das/` DAS, `etc/` other, `cs/` computing).
3. **Build the entry from the PDF**: title page and journal header first; DOI resolved (Crossref) for volume,
   issue, pages, year. Fields you cannot verify are left out, never guessed. Publisher `.ris` ->
   `python3 scripts/ris2bib.py file.ris --key <Key>`; then verify every field the same way.
4. **ASCII and escapes**: match the target bib (mybible's bibs are checked for non-ASCII: use LaTeX escapes
   such as `{\"o}`, `{\v{a}}`); protect capitals in titles with braces (`{FWI}`, `{G}auss-{N}ewton`).
5. **Check**: no duplicate keys across the five bibs (`grep -h '^@' *.bib | sort | uniq -d`); run
   `python3 scripts/check_citations.py --strict` in `mypaper/mybible` (0 ghost keys, 0 manual "(Name, year)"
   citations, 0 duplicate keys) and compile with 0 undefined citations.

## Rules

- **No ghost citations**: every `\cite` key exists, and its PDF is on disk and was read (`benz:paper-read`).
- **No manual in-text citations**: natbib `\citet`/`\citep`/`\citeauthor` everywhere, including tables,
  captions and TikZ.
- An entry added before its PDF is read carries `note = {UNVERIFIED: PDF not yet read (YYYY-MM-DD)}`, removed
  only after reading.
- Software is cited by its paper (and the repo URL in a footnote or `howpublished`), with the licence's
  citation clause honoured (e.g. occamypy: cite in the paper).
