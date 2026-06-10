#!/usr/bin/env bash
#
# install-omp-skills.sh
#
# Install this checkout's skills for Oh My Pi (omp) native skill discovery.
#
# omp discovers user skills directly under ~/.omp/agent/skills. Each
# Superfastpowers skill is installed as its own symlink or copy, for example
# ~/.omp/agent/skills/brainstorming -> this checkout's skills/brainstorming.
#
# Usage:
#   ./scripts/install-omp-skills.sh                   # symlink each skill into ~/.omp/agent/skills
#   ./scripts/install-omp-skills.sh --copy            # copy skills instead of symlinking
#   ./scripts/install-omp-skills.sh --force           # replace existing skill targets
#   ./scripts/install-omp-skills.sh --target DIR      # install into another skills directory
#   ./scripts/install-omp-skills.sh --project         # install into ./.omp/skills
#   ./scripts/install-omp-skills.sh --dry-run         # show actions without changing files
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/skills"
TARGET_ROOT="${OMP_PROCESSING_AGENT_DIR:-$HOME/.omp/agent}/skills"
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
    --project)
      TARGET_ROOT="$REPO_ROOT/.omp/skills"
      shift
      ;;
    --target)
      [[ $# -ge 2 ]] || die "--target requires a path"
      TARGET_ROOT="$2"
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

replace_target() {
  local target="$1"

  if [[ -L "$target" ]]; then
    run rm "$target"
  elif [[ -e "$target" ]]; then
    run rm -rf "$target"
  fi
}

run mkdir -p "$TARGET_ROOT"

OLD_PACK_TARGET="$TARGET_ROOT/superfastpowers"
if [[ -L "$OLD_PACK_TARGET" && "$(readlink "$OLD_PACK_TARGET")" == "$SOURCE" ]]; then
  run rm "$OLD_PACK_TARGET"
fi

installed_count=0

for skill_source in "$SOURCE"/*; do
  [[ -d "$skill_source" ]] || continue
  [[ -f "$skill_source/SKILL.md" ]] || continue

  skill_name="$(basename "$skill_source")"
  target="$TARGET_ROOT/$skill_name"

  if [[ -e "$target" || -L "$target" ]]; then
    if [[ -L "$target" && "$(readlink "$target")" == "$skill_source" ]]; then
      log "OMP skill already installed: $target -> $skill_source"
      installed_count=$((installed_count + 1))
      continue
    fi

    [[ "$FORCE" -eq 1 ]] || die "target already exists at $target; rerun with --force to replace it"
    replace_target "$target"
  fi

  case "$MODE" in
    symlink)
      run ln -s "$skill_source" "$target"
      ;;
    copy)
      run mkdir -p "$target"
      run cp -R "$skill_source/." "$target/"
      ;;
    *)
      die "unknown install mode: $MODE"
      ;;
  esac

  installed_count=$((installed_count + 1))
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "Would install $installed_count Superfastpowers skills for OMP into $TARGET_ROOT"
else
  log "Installed $installed_count Superfastpowers skills for OMP into $TARGET_ROOT"
  log "Restart omp so it reloads native skills."
fi
