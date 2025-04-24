#!/bin/bash

# Detect network diaposon (ex. 192.168.1.0/24)
NETWORK="192.168.1.0/24"

# File for store known devices
KNOWN_DEVICES="$HOME/.known_devices.txt"

# File for store current devices
CURRENT_DEVICES="$HOME/.current_devices.txt"

# Scan network devices
arp-scan --localnet | awk '/:/{print $2}' | sort > "$CURRENT_DEVICES"

# Save current devices list
if [ ! -f "$KNOWN_DEVICES" ]; then
    cp "$CURRENT_DEVICES" "$KNOWN_DEVICES"
    echo "🔍 List of current devices saved."
    exit 0
fi

# Search new devices
NEW_DEVICES=$(comm -13 "$KNOWN_DEVICES" "$CURRENT_DEVICES")

if [ -n "$NEW_DEVICES" ]; then
    echo "🚨 Detected new devices in network:"
    echo "$NEW_DEVICES"
    notify-send "New devices in network" "$NEW_DEVICES"
    echo "$NEW_DEVICES" >> "$KNOWN_DEVICES"
else
    echo "✅ New devices in net not found."
fi

# Обновляем список известных устройств
mv "$CURRENT_DEVICES" "$KNOWN_DEVICES"
