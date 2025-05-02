#!/usr/bin/env bash

# Log file for events
LOG_FILE="$HOME/.network_changes.log"

# Previous IP address
PREV_IP=""

while true; do
    # Get current IP
    CURRENT_IP=$(curl -s ifconfig.me)

    # Send message if IP is changing
    if [ "$CURRENT_IP" != "$PREV_IP" ]; then
        MESSAGE="⚠️ Detect Changing IP: $CURRENT_IP"
        echo "$(date) $MESSAGE" | tee -a "$LOG_FILE"
        notify-send "Network Alert" "$MESSAGE"
        PREV_IP="$CURRENT_IP"
    fi

    sleep 60  # Проверяем каждую минуту
done
