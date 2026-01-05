#!/usr/bin/env bash

MOUNT_DIR="$HOME/MOUNTED_DEVICE"

mkdir -p "$MOUNT_DIR"

DEVICE=$(lsblk -o NAME,TYPE,HOTPLUG | awk '$2 == "disk" && $3 == 1 {print $1}' | tail -n1)

if [ -n "$DEVICE" ]; then
    PARTITION="/dev/${DEVICE}1"

    mkdir -p "$MOUNT_DIR/$PARTITION"
    sudo mount "$PARTITION" "$MOUNT_DIR/$PARTITION"

    echo "✅ Device $PARTITION mounted to $MOUNT_DIR/$PARTITION"
else
    echo "❌ USB-device not found"
fi
