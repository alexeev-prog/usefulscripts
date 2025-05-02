#!/usr/bin/env bash

# Target directory for scan
TARGET_DIR="$HOME"

# Search and delete broken symlinks
find "$TARGET_DIR" -xtype l -print -delete

echo "✅ All broken symlinks deleted from $TARGET_DIR"
