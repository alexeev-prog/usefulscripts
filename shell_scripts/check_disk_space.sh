#!/usr/bin/env bash

THRESHOLD=90
LOG_FILE="$HOME/.disk_usage.log"

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -ge "$THRESHOLD" ]; then
    MESSAGE="⚠️ Disk space is used by $DISK_USAGE%!"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "Disk Alert" "$MESSAGE"
fi
