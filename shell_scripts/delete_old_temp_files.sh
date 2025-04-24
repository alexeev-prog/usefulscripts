#!/bin/bash

# Directory for clean
TARGET_DIR="/tmp"

# Max age of file in days
MAX_AGE=7

# Delete files that are more MAX_AGE ago
find "$TARGET_DIR" -type f -mtime +$MAX_AGE -exec rm -v {} \;

echo "✅ Delete temporary files that are more $MAX_AGE days from $TARGET_DIR"
