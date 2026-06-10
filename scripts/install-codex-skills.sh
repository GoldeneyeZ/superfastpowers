#!/usr/bin/env bash
#
# install-codex-skills.sh
#
# Install this checkout's skills for Codex native skill discovery.
#
# Codex discovers shared agent skills from ~/.agents/skills. Superfastpowers is
# installed as a skill pack at ~/.agents/skills/superfastpowers, pointing at this
# checkout's skills/ directory.
#
# Usage:
#   ./scripts/install-codex-skills.sh                 # symlink skills into ~/.agents/skills
#   ./scripts/install-codex-skills.sh --copy          # copy skills instead of symlinking
#   ./scripts/install-codex-skills.sh --force         # replace existing target
#   ./scripts/install-codex-skills.sh --target PATH   # install somewhere else
#   ./scripts/install-codex-skills.sh --dry-run       # show actions without changing files
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/skills"
TARGET_ROOT="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
TARGET="$TARGET_ROOT/superfastpowers"
MODE="symlink"
FORCE=0
DRY_RUN=0

usage() {
  sed -n '/^# Usage:/,$s/^# \{0,1\}//p' "$0" | sed '/^set -euo pipefail/,$d'
  exit "${1:-0}"
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

log() {
  echo "$*"
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf 'DRY-RUN:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)
      MODE="copy"
      shift
      ;;
    --symlink)
      MODE="symlink"
      shift
      ;;
    --force|-f)
      FORCE=1
      shift
      ;;
    --dry-run|-n)
      DRY_RUN=1
      shift
      ;;
    --target)
      [[ $# -ge 2 ]] || die "--target requires a path"
      TARGET="$2"
      TARGET_ROOT="$(dirname "$TARGET")"
      shift 2
      ;;
    --help|-h)
      usage 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage 2
      ;;
  esac
done

[[ -d "$SOURCE" ]] || die "skills directory not found at $SOURCE"
[[ -f "$SOURCE/using-superfastpowers/SKILL.md" ]] || die "expected bootstrap skill missing at $SOURCE/using-superfastpowers/SKILL.md"

replace_existing_target() {
  if [[ -L "$TARGET" ]]; then
    run rm "$TARGET"
  elif [[ -e "$TARGET" ]]; then
    run rm -rf "$TARGET"
  fi
}

if [[ -e "$TARGET" || -L "$TARGET" ]]; then
  if [[ -L "$TARGET" ]]; then
    EXISTING="$(readlink "$TARGET")"
    if [[ "$EXISTING" == "$SOURCE" ]]; then
      log "Codex skills already installed: $TARGET -> $SOURCE"
      exit 0
    fi
  fi

  [[ "$FORCE" -eq 1 ]] || die "target already exists at $TARGET; rerun with --force to replace it"
  replace_existing_target
fi

run mkdir -p "$TARGET_ROOT"

case "$MODE" in
  symlink)
    run ln -s "$SOURCE" "$TARGET"
    ;;
  copy)
    run mkdir -p "$TARGET"
    run cp -R "$SOURCE/." "$TARGET/"
    ;;
  *)
    die "unknown install mode: $MODE"
    ;;
esac

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "Would install Superfastpowers skills for Codex at $TARGET"
else
  log "Installed Superfastpowers skills for Codex at $TARGET"
  log "Restart Codex so it reloads native skills."
fi
