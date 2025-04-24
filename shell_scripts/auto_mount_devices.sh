#!/bin/bash

# Mountpoint
MOUNT_DIR="$HOME/MOUNTED_DEVICE"

# Create dir
mkdir -p "$MOUNT_DIR"

# Search a new device for mount
DEVICE=$(lsblk -o NAME,TYPE,HOTPLUG | awk '$2 == "disk" && $3 == 1 {print $1}' | tail -n1)

# If device is found
if [ -n "$DEVICE" ]; then
    # Получаем раздел (например, sdb1)
    PARTITION="/dev/${DEVICE}1"

    # Mount DEVICE
    mkdir -p "$MOUNT_DIR/$PARTITION"
    sudo mount "$PARTITION" "$MOUNT_DIR/$PARTITION"

    echo "✅ Device $PARTITION mounted to $MOUNT_DIR/$PARTITION"
else
    echo "❌ USB-device not found"
fi
