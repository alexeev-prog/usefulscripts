#!/usr/bin/env bash

THRESHOLD=80
LOG_FILE="$HOME/.cpu_usage.log"

CPU_LOAD=$(awk '{print $1}' < /proc/loadavg | awk '{print $1*100}')

if (( ${CPU_LOAD%.*} >= THRESHOLD )); then
    MESSAGE="⚠️ High CPU Usage: $CPU_LOAD%"
    echo "$MESSAGE" | tee -a "$LOG_FILE"
    notify-send "CPU Alert" "$MESSAGE"
fi
