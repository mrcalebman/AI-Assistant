#!/bin/bash

# Weekly check — runs at SessionStart.
# Outputs reminder text if /audit or /level-up is 7+ days overdue.
# Claude reads this output and surfaces the reminder to Caleb.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

AUDIT_FILE="$PROJECT_DIR/last-audit.txt"
LEVELUP_FILE="$PROJECT_DIR/last-level-up.txt"

TODAY=$(date +%Y-%m-%d)
TODAY_EPOCH=$(date -d "$TODAY" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$TODAY" +%s)

days_since() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo 999
    return
  fi
  local last_date
  last_date=$(cat "$file" | tr -d '[:space:]')
  local last_epoch
  last_epoch=$(date -d "$last_date" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$last_date" +%s 2>/dev/null)
  if [ -z "$last_epoch" ]; then
    echo 999
    return
  fi
  echo $(( (TODAY_EPOCH - last_epoch) / 86400 ))
}

AUDIT_DAYS=$(days_since "$AUDIT_FILE")
LEVELUP_DAYS=$(days_since "$LEVELUP_FILE")

REMINDERS=""

if [ "$AUDIT_DAYS" -ge 7 ]; then
  REMINDERS="$REMINDERS\n- /audit is overdue (last run: ${AUDIT_DAYS} days ago). Run it this session."
fi

if [ "$LEVELUP_DAYS" -ge 7 ]; then
  REMINDERS="$REMINDERS\n- /level-up is overdue (last run: ${LEVELUP_DAYS} days ago). Run it this session."
fi

if [ -n "$REMINDERS" ]; then
  echo "WEEKLY REMINDERS:"
  echo -e "$REMINDERS"
fi
