#!/usr/bin/env bash
# find-plan.sh — Deterministic plan file helper for development-skills plugin
# Usage:
#   find-plan.sh active     — Find in-progress plan, print filename + WORKFLOW STATE
#   find-plan.sh next       — Print the next NNNN number for a new plan file
#   find-plan.sh active-or-next — Print active plan info if exists, otherwise next number
set -euo pipefail

PLANS_DIR="docs/plans"

find_active() {
  if [ ! -d "$PLANS_DIR" ]; then
    echo "NO_ACTIVE_PLAN"
    return 0
  fi

  local found=0
  # Match ANY .md file in plans dir (not just implementation_plan)
  for f in "$PLANS_DIR"/*.md; do
    [ -f "$f" ] || continue
    # Skip research files
    [[ "$(basename "$f")" == *__research.md ]] && continue
    if grep -qi "Status:.*In Progress" "$f" 2>/dev/null; then
      if [ "$found" -gt 0 ]; then
        echo "WARNING: Multiple active plans found. Using first match."
        break
      fi
      echo "ACTIVE_PLAN: $f"
      # Extract WORKFLOW STATE block: from ## WORKFLOW STATE to next ## heading or blank line
      awk '/^## WORKFLOW STATE/{found=1; next} found && /^## /{exit} found && /^$/{exit} found{print}' "$f"
      found=1
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "NO_ACTIVE_PLAN"
  fi
}

find_next_number() {
  if [ ! -d "$PLANS_DIR" ]; then
    echo "0001"
    return 0
  fi

  local last
  last=$(for f in "$PLANS_DIR"/*.md; do [ -f "$f" ] && basename "$f"; done 2>/dev/null | grep -oE '^[0-9]+' | sort -n | tail -1)
  if [ -z "${last:-}" ]; then
    echo "0001"
  else
    printf "%04d\n" $((10#$last + 1))
  fi
}

case "${1:-}" in
  active)
    find_active
    ;;
  next)
    find_next_number
    ;;
  active-or-next)
    find_active
    echo "---"
    echo "NEXT_NUMBER: $(find_next_number)"
    ;;
  *)
    echo "Usage: $0 {active|next|active-or-next}" >&2
    exit 1
    ;;
esac
