#!/usr/bin/env bash

# Threshold of CPU Usage
THRESHOLD=80
# Log file
LOG_FILE="$HOME/.cpu_usage.log"

# Get middle of CPU Usage
CPU_LOAD=$(awk '{print $1}' < /proc/loadavg | awk '{print $1*100}')

if (( ${CPU_LOAD%.*} >= THRESHOLD )); then
    MESSAGE="⚠️ High CPU Usage: $CPU_LOAD%"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "CPU Alert" "$MESSAGE"
fi
