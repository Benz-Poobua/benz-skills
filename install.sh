#!/usr/bin/env bash
# install.sh — make the `benz` plugin (and the caveman companion) available in every Claude Code session.
#
#   bash install.sh            # register this directory as a local marketplace, install plugin `benz` (user scope)
#   bash install.sh --check    # show what is installed; change nothing
#   bash install.sh --symlink  # fallback without the plugin system: link skills into ~/.claude/skills (unprefixed names)
#   bash install.sh --update   # after editing skills: bump patch version, validate, refresh the installed copy
#
# Why a plugin: project-level .claude/skills are searched only up to each repo's git root, so a folder above the
# repos (Imaging_Project/.claude/skills) is never seen from inside das_ani etc. A user-scope plugin is seen from
# every directory and ships the agents too. The install is a COPY in ~/.claude/plugins/cache: after editing,
# run `bash install.sh --update` (version bump + refresh; tested 2026-11-10) and start a new session.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-install}"

have_claude() { command -v claude >/dev/null 2>&1; }

check() {
  echo "== plugin manifests"
  python3 -c "import json;json.load(open('$HERE/.claude-plugin/plugin.json'));json.load(open('$HERE/.claude-plugin/marketplace.json'));print('json ok')"
  if have_claude; then
    echo "== claude plugin validate"; claude plugin validate "$HERE" || true
    echo "== installed plugins"; claude plugin list 2>/dev/null || true
  else
    echo "claude CLI not on PATH (in the desktop app, run the commands below in a terminal that has it)"
  fi
  echo "== ~/.claude/skills"; ls -la "$HOME/.claude/skills" 2>/dev/null || echo "(none)"
}

case "$MODE" in
  --check) check ;;
  --symlink)
    mkdir -p "$HOME/.claude/skills"
    for d in "$HERE"/skills/*/; do
      n="$(basename "$d")"; ln -sfn "$d" "$HOME/.claude/skills/$n"; echo "linked $n"
    done
    echo "agents are not linked (symlinked agents are not documented); copy agents/*.md to ~/.claude/agents/ if wanted"
    ;;
  install)
    have_claude || { echo "claude CLI not found; install Claude Code CLI or use: bash install.sh --symlink"; exit 1; }
    claude plugin validate "$HERE"
    claude plugin marketplace add "$HERE"
    claude plugin install benz@benz-skills
    # companion: caveman (terse output), default on via its SessionStart hook
    if ! claude plugin list 2>/dev/null | grep -q '^.*caveman'; then
      claude plugin marketplace add JuliusBrussee/caveman || true
      claude plugin install caveman@caveman || true
    fi
    echo "done. Start a new session (or /reload-plugins); skills appear as /benz:<name>, agents as benz:<name>."
    ;;
  --update)
    # The install is a COPY in ~/.claude/plugins/cache; `claude plugin update` only refreshes it after a version
    # bump (tested 2026-11-10). Bump the patch version, validate, refresh.
    have_claude || { echo "claude CLI not found"; exit 1; }
    PJ="$HERE/.claude-plugin/plugin.json"
    NEW=$(python3 - "$PJ" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
a, b, c = (int(x) for x in d["version"].split("."))
d["version"] = f"{a}.{b}.{c + 1}"
open(p, "w").write(json.dumps(d, indent=2) + "\n")
print(d["version"])
PY
)
    echo "version -> $NEW"
    claude plugin validate "$HERE"
    claude plugin marketplace update benz-skills
    claude plugin update benz@benz-skills
    echo "refreshed to $NEW. Start a new session to load it; commit + push so others can update."
    ;;
  *) echo "usage: bash install.sh [--check|--symlink|--update]"; exit 2 ;;
esac
