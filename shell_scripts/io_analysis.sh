#!/usr/bin/env bash

echo "=== Disk I/O Analysis and File Descriptor Search ==="
echo "Timestamp: $(date)"
echo ""

echo "1. General I/O Statistics (first 3 seconds average, then live):"
echo "------------------------------------------------------------------"
if command -v iostat &> /dev/null; then
  iostat -dx 1 3
else
  echo "Utility 'iostat' not installed. Install package 'sysstat'."
fi
echo ""

echo "2. Disk Space Usage:"
echo "---------------------------------------"
df -h | sort -k5 -hr
echo ""

echo "3. Processes with Active Disk Load (KB/sec):"
echo "--------------------------------------------------"
if command -v pidstat &> /dev/null; then
  pidstat -dl 1 1 | sort -k6 -nr | head -15
else
  echo "Utility 'pidstat' not installed. Install package 'sysstat'."
  echo "Alternative: use /proc//io (more complex parsing)."
fi
echo ""

echo "4. Top 10 Processes by Number of Open File Descriptors:"
echo "---------------------------------------------------------------"
for pid in $(ps -eo pid --no-headers); do
  if [ -d /proc/$pid/fd ]; then
    fd_count=$(ls -1 /proc/$pid/fd 2>/dev/null | wc -l)
    proc_name=$(ps -p $pid -o comm= 2>/dev/null)
    if [ -n "$proc_name" ]; then
      echo "PID: $pid, Name: $proc_name, FD: $fd_count"
    fi
  fi
done | sort -t',' -k3 -nr | head -10
echo ""

echo "5. Processes with Large Open Files (>100MB):"
echo "-------------------------------------------------"
for pid in $(ps -eo pid --no-headers); do
  if [ -d /proc/$pid/fd ]; then
    for fd in /proc/$pid/fd/*; do
      file_size=$(stat -Lc%s "$fd" 2>/dev/null)
      if [ -n "$file_size" ] && [ "$file_size" -gt 104857600 ]; then
        file_name=$(readlink -f "$fd" 2>/dev/null)
        proc_name=$(ps -p $pid -o comm= 2>/dev/null)
        file_size_mb=$((file_size / 1024 / 1024))
        echo "PID: $pid, Process: $proc_name, File: $file_name, Size: ~$file_size_mb MB"
      fi
    done
  fi
done
