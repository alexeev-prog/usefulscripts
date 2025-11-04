#!/usr/bin/env bash
WIN_MIN=${1:-60}
LOG="/var/log/coredumps_watch.log"
echo "$(date) — core dumps (last ${WIN_MIN}m)" | tee -a "$LOG"

if command -v coredumpctl >/dev/null 2>&1; then
  LIST=$(coredumpctl list --since "-${WIN_MIN} min" --no-pager 2>/dev/null | sed '1,1d')
  if [ -n "$LIST" ]; then
    echo "$LIST" | tee -a "$LOG"
    LAST_JOURNAL=$(echo "$LIST" | tail -n1 | awk '{print $1" "$2" "$3" "$4" "$5}')
    coredumpctl info --no-pager $(echo "$LAST_JOURNAL" | awk '{print $1" "$2" "$3}') 2>/dev/null \
      | sed 's/^/  /' | tee -a "$LOG"
  else
    echo "OK: New Core dumps not founds" | tee -a "$LOG"
  fi
else
  FOUND=$(find /var/lib/systemd/coredump /var/crash -type f -mmin -"$WIN_MIN" 2>/dev/null)
  [ -n "$FOUND" ] && echo "$FOUND" | tee -a "$LOG" || echo "OK: New Core dumps not founds" | tee -a "$LOG"
fi
