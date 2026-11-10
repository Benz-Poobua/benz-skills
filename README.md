# benz-skills

Claude Code plugin **`benz`**: evidence-first research skills for DAS interferometry / FWI software and
for honest paper work, plus four subagents with fixed model tiers. Built for the `Imaging_Project`
ecosystem of Benz Poobua (Stanford Geophysics / SEP). MIT licence.

## Install (once per machine)

On Benz's Mac (local folder as the marketplace):

```bash
bash ~/Desktop/Imaging_Project/benz-skills/install.sh
```

It validates the plugin, adds this folder as the marketplace `benz-skills`, installs `benz@benz-skills` at
user scope and makes sure the `caveman` companion plugin is installed. Check with `claude plugin list`.

Anywhere else (a collaborator, another laptop, Sherlock), from GitHub:

```bash
claude plugin marketplace add Benz-Poobua/benz-skills
claude plugin install benz@benz-skills
```

Why a plugin and not `Imaging_Project/.claude/skills`: Claude Code searches project skills only up to each
repository's git root, so a folder above the repos is invisible from inside `das_ani/`, `mfold/`, ... A
user-scope plugin is visible in every folder, carries the agents, and works in the terminal and in the
desktop app's Code tab. Fallback without the plugin system: `bash install.sh --symlink` (links skills into
`~/.claude/skills/`, unprefixed names, no agents).

## Is it automatic?

Yes. Once installed, every NEW session (terminal `claude` or the desktop app, any folder) loads the 18 skill
descriptions (~2,000 tokens) and the 4 agents. Claude calls a skill by itself when the request matches its
description ("read this paper", "this run will take hours", "review this diff", "add this bib entry").
You can also call one explicitly: `/benz:<skill>`, e.g. `/benz:core-ledger`, `/benz:paper-read`. Agents are
used by name: "use benz:reader on <pdf>", "have benz:verifier re-check this". Inside `Imaging_Project`, the root
`CLAUDE.md` (rules) loads automatically as well, and a repo's own `CLAUDE.md` loads when you start in it.
The `caveman` terse style stays on through its own plugin.

## Continue a project

1. Start the session **inside the repo** (`cd ~/Desktop/Imaging_Project/das_ani && claude`, or choose that
   folder in the desktop app).
2. Say "continue" — or paste the restart prompt at the bottom of that repo's `TASKS.md`. Claude reads
   `CLAUDE.md` (automatic), the top block of `TASKS.md` and the newest `LEDGER.md` entry, and runs the repo's
   first command (usually the tests) before changing anything.
3. At the end of a work block say "update the ledger" (or `/benz:core-ledger`): Claude prepends a `LEDGER.md`
   entry and updates `TASKS.md`.

## Start a new project

1. Start a session in `~/Desktop/Imaging_Project` and describe it: "new repo `<name>` for `<goal>`, house style".
2. Claude follows `/benz:code-house-style` (das_ani layout, module headers, config helpers, plot style) and
   `/benz:core-ledger` (creates `CLAUDE.md`, `TASKS.md`, `LEDGER.md` from the templates), registers the repo in
   the root `PATHS.md` and `STATUS.md`, and asks before `git init` / creating a GitHub repo.
3. Its paper goes to `mypaper/<name>/`; published methods go into the FWI Book first (`/benz:paper-write`).

## Edit a skill, then refresh

The install keeps a COPY in `~/.claude/plugins/cache/benz-skills/benz/<version>/`; edits here reach sessions
only after a refresh:

```bash
bash ~/Desktop/Imaging_Project/benz-skills/install.sh --update   # bumps 0.1.x -> 0.1.(x+1), validates, refreshes the copy
# (by hand: bump "version" in .claude-plugin/plugin.json; claude plugin validate <dir>;
#  claude plugin marketplace update benz-skills; claude plugin update benz@benz-skills)   then start a new session
git -C ~/Desktop/Imaging_Project/benz-skills push   # so collaborators get it (they run the same two update commands)
```

## Index

Skills and agents: [`PATHS.md`](PATHS.md). Rules for editing: [`CLAUDE.md`](CLAUDE.md).
Provenance and licences of adapted material: [`docs/SOURCES.md`](docs/SOURCES.md).

- **Core** (`core-*`): evidence labels, subagent delegation with model tiers, the CLAUDE.md / TASKS.md /
  LEDGER.md discipline, and resumable offline long runs (caffeinate, guard, resume) that Benz launches himself.
- **Code** (`code-*`): house style from `das_ani`, numerical gates, correct-then-fast, debugging, review,
  generated notebooks, licence-aware extraction, SLURM.
- **Paper** (`paper-*`): line-by-line reading with page/equation numbers, BibTeX hygiene with the
  `Lastname_etal_YYYY` convention, book-first writing (published work only), number tracing, reproducible
  figures, the five-question test for adopting a published method.
