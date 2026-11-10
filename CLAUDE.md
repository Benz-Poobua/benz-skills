# benz-skills — RULES for the skill library (read before editing a skill)

> Claude Code plugin **`benz`** (marketplace `benz-skills`): Benz Poobua's skills and model-tiered subagents for
> the Imaging_Project ecosystem. Index: `PATHS.md`. Install/use: `README.md`. Provenance and licences of
> adapted material: `docs/SOURCES.md`. Git repo, MIT, remote `git@github.com:Benz-Poobua/benz-skills.git`.

## 0. What this is

Two parts plus a core, one plugin:

| part | skills | for |
|---|---|---|
| **core** | `core-evidence`, `core-delegate`, `core-ledger`, `core-long-run` | every session: evidence, subagents and model tiers, CLAUDE/TASKS/LEDGER, offline runs |
| **code** | `code-house-style`, `code-verify`, `code-fast`, `code-debug`, `code-review`, `code-notebooks`, `code-extract`, `code-hpc` | research software (das_ani is the style reference) |
| **paper** | `paper-read`, `paper-bib`, `paper-write`, `paper-numbers`, `paper-figures`, `paper-adopt` | papers, books, citations (FWI Book first, published work only) |
| **agents** | `surveyor` (haiku), `reader` (sonnet), `builder` (sonnet), `verifier` (opus) | delegation with fixed model tiers |

Invoked as `/benz:<skill>` or automatically from each skill's `description`; agents as `benz:<agent>`.
Repo-specific skills stay in their repos (`<repo>/skills/`); this plugin holds only what every repo shares.

## 1. Rules for editing this library

1. **One meaning, one home.** A rule lives in exactly one skill; other skills point at it (`benz:<name>`).
   Repo CLAUDE.md files point here instead of restating generic discipline.
2. **Descriptions are always loaded** (every session pays for them): front-load the trigger words, one trigger
   per real branch, <= ~350 characters, no identity the body already carries.
3. **Bodies are short** (target <= 120 lines): steps with completion criteria first, reference after;
   long material goes to `references/` or `scripts/` next to the SKILL.md.
4. **State the positive behaviour** ("write one-line comments") rather than a list of prohibitions; keep a
   prohibition only for hard guardrails (git, deletion, licences, secrets).
5. **Every path, script and number in a skill must exist and be true.** Scripts are run once before they are
   referenced; `python3 skills/core-ledger/scripts/check_doc_paths.py <file>` checks backticked paths.
6. **Adapted material is credited** in `docs/SOURCES.md` (repo, commit, licence). No-licence sources
   contribute ideas only, re-written in our words; MIT/Apache text may be adapted with attribution.
7. **Validate after any change**: `claude plugin validate .` (when the CLI is available) and the JSON check
   `python3 -c "import json;json.load(open('.claude-plugin/plugin.json'));json.load(open('.claude-plugin/marketplace.json'))"`.
   The install is a COPY (`~/.claude/plugins/cache/benz-skills/benz/<version>/`): after editing, run
   `bash install.sh --update` (bumps the patch version, validates, refreshes the copy), then start a new session.
8. **A skill that changes no decision is deleted** (net-count rule): when adding a skill, say which mistake
   or cost it prevents, in `docs/SOURCES.md` or its description.
9. Git: commit only when Benz asks; `git add <paths>`.

## 2. Output style (applies with this plugin)

The `caveman` plugin (JuliusBrussee/caveman, MIT) is installed at user scope and on by default through its
SessionStart hook (level full): terse chat. **Normal prose** for code, commit messages, docstrings, READMEs,
CLAUDE.md files, manuscripts, books, security warnings and irreversible-action confirmations.

## 3. Layout

```
benz-skills/
  .claude-plugin/marketplace.json   marketplace "benz-skills" -> plugin "benz" (source "./")
  .claude-plugin/plugin.json        plugin "benz"
  skills/<name>/SKILL.md            + references/, scripts/, templates/, tools/ per skill
  agents/{surveyor,reader,builder,verifier}.md
  CLAUDE.md PATHS.md README.md install.sh docs/SOURCES.md LICENSE
```
