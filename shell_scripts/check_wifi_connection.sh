#!/bin/bash

# Файл для хранения последней сети
LAST_SSID_FILE="$HOME/.last_ssid"

# Get current SSID
CURRENT_SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)

if [ ! -f "$LAST_SSID_FILE" ]; then
    echo "$CURRENT_SSID" > "$LAST_SSID_FILE"
    exit 0
fi

PREV_SSID=$(cat "$LAST_SSID_FILE")

if [ "$CURRENT_SSID" != "$PREV_SSID" ]; then
    MESSAGE="🔄 Connect to new WiFi: $CURRENT_SSID"
    echo "$(date) $MESSAGE" | tee -a "$HOME/wifi_changes.log"
    notify-send "Wi-Fi Alert" "$MESSAGE"
    echo "$CURRENT_SSID" > "$LAST_SSID_FILE"
fi
