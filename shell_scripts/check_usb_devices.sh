#!/usr/bin/env bash

LOG_FILE="/var/log/usb_changes.log"
STATE_FILE="/var/lib/usb_changes/usb_state.txt"

mkdir -p /var/lib/usb_changes

echo "🔍 Searching installed USB... $(date)" | tee -a "$LOG_FILE"

lsusb > /tmp/current_usb.txt

if [ ! -f "$STATE_FILE" ]; then
    cp /tmp/current_usb.txt "$STATE_FILE"
    echo "📦 First save for USB" | tee -a "$LOG_FILE"
    exit 0
fi

if ! diff "$STATE_FILE" /tmp/current_usb.txt >/dev/null; then
    echo "⚠️  USB Connections changed" | tee -a "$LOG_FILE"
    echo "--- After:" | tee -a "$LOG_FILE"
    cat "$STATE_FILE" | tee -a "$LOG_FILE"
    echo "--- Before:" | tee -a "$LOG_FILE"
    cat /tmp/current_usb.txt | tee -a "$LOG_FILE"
    cp /tmp/current_usb.txt "$STATE_FILE"
else
    echo "✅ USB Connections not changed" | tee -a "$LOG_FILE"
fi

rm /tmp/current_usb.txt
