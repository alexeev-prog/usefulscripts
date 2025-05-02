#!/usr/bin/env bash

# Threshold of disk usage
THRESHOLD=90
# Log file
LOG_FILE="$HOME/.disk_usage.log"

# Get root disk partition usage percent
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -ge "$THRESHOLD" ]; then
    MESSAGE="⚠️ Disk space is used by $DISK_USAGE%!"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "Disk Alert" "$MESSAGE"
fi
