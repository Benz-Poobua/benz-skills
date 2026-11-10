---
name: paper-read
description: Line-by-line reading of a paper, thesis, manual or book chapter with exact page, equation, figure and table numbers - no skimming, signs checked on the rendered page, a reading note written to disk. Use whenever a PDF is read to cite it, extract a method or equation, check a claim, or feed the FWI Book or a manuscript; and when delegating reading to the benz:reader agent.
---

# paper-read

A citation is only as good as the reading behind it. Read every line of what you cite; never cite
what you did not open; never attribute an equation you did not see on the page.

## Steps

1. **Locate and identify.** Find the PDF on disk (`mypaper/mybible/{alg,etc,fwi,das,cs}/`,
   `inspiring_papers/`, a repo's `papers/`). Take the full reference **from the PDF itself** (title page,
   journal header, DOI). Record the **page offset** (printed page vs PDF page) once, e.g. "PDF p = printed p + 17".
2. **Read it all, in order**, including appendices and supplementary material, in chunks of <= 20 PDF pages
   (`Read` with `pages=`; `pdftotext -layout -f a -l b` for search). Completion: every page was opened;
   the note says which pages were read.
3. **Check symbols on the rendered page** wherever a sign, conjugate, prime, transpose, hat or bar matters
   (`pdftotext` drops overbars and primes): read the page image. Write which equations were checked this way.
4. **Write the reading note** (`references/note_template.md`) to the project's notes folder
   (`mypaper/mybible/notes/<Key>.md`, or the repo's `docs/notes/<Key>.md`): claims with page + eq/fig/table;
   assumptions; method equations transcribed with their numbers and conventions (Fourier sign, units);
   data and numbers reported; limitations the authors state; what we can use; what we must not claim.
5. **Mark uncertainty**: anything not verified on the page is written as UNVERIFIED in the note, and an
   unverifiable pointer is dropped from the text (keep the citation, drop the "eq. N") rather than guessed.

## Rules

- Quote at most 15 words of any source, in quotation marks, with page; otherwise paraphrase.
- Separate "the paper claims" from "we verified" in every note and every manuscript sentence.
- Cite the book (FWI Book) by `\label`, never by page/chapter number (it renumbers).
- When delegating: use the `benz:reader` agent with the PDF path, page range, the questions, and the note
  path; require page/eq for every statement; re-check two of its pointers yourself (`benz:core-delegate`).
- Venue red flags (non-peer-reviewed preprint servers of unknown standing) are recorded in the note; such
  papers are not cited as evidence.
