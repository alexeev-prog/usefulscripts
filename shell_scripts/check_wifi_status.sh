#!/usr/bin/env bash

# Host for check (Google DNS)
PING_HOST="8.8.8.8"
# Log file
LOG_FILE="$HOME/.network_status.log"

# Check internet connection
if ! ping -c 1 "$PING_HOST" &>/dev/null; then
    MESSAGE="⚠️ Internet is not available!"
    echo "$(date) $MESSAGE" | tee -a "$LOG_FILE"
    notify-send "Network Alert" "$MESSAGE"
else
    MESSAGE="Internet is available!"
    echo "$(date) $MESSAGE" | tee -a "$LOG_FILE"
    notify-send "Network Alert" "$MESSAGE"
fi
