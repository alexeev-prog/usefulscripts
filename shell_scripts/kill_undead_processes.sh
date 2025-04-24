#!/bin/bash

# Threshold of frozed processes
THRESHOLD=600

# Search and kill frozed processes
ps -eo pid,etimes,comm --no-headers | while read pid etime command; do
    if [ "$etime" -gt "$THRESHOLD" ]; then
        echo "Process $command (PID $pid) is frozen! Killing..."
        kill -9 "$pid"
    fi
done
