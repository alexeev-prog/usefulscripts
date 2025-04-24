#!/bin/bash

# Log file for events
LOG_FILE="$HOME/.usb_disconnect.log"

# Monitoring USB Events
udevadm monitor --subsystem-match=usb | while read line; do
    if echo "$line" | grep -q "remove"; then
        MESSAGE="⚠️ USB-device is disconnected!"
        echo "$(date) $MESSAGE" | tee -a "$LOG_FILE"
        notify-send "USB Alert" "$MESSAGE"
    fi
done
