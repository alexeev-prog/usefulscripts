#!/usr/bin/env bash

echo "=== Memory Analysis and OOM Killer Candidate Processes ==="
echo "Timestamp: $(date)"
echo ""

echo "1. Memory Summary:"
echo "-------------------"
free -h
echo ""

echo "2. Detailed RAM and Swap Usage:"
echo "----------------------------------------"
cat /proc/meminfo | grep -E "(MemTotal|MemAvailable|SwapTotal|SwapFree|SwapCached)"
echo ""

echo "3. Top 10 Processes by Resident Memory (RSS) Usage:"
echo "-------------------------------------------------------------"
ps aux --sort=-%mem | awk 'NR<=11 {printf "%-8s %-6s %-4s %-8s %-8s %s\n", $2, $1, $4, $3, $6/1024" MB", $11}'
echo ""

echo "4. Processes with Large Amounts of Dirty Memory:"
echo "------------------------------------------------------------------"
for pid in $(ps -eo pid --no-headers); do
  if [ -f /proc/$pid/statm ]; then
    dirty_pages=$(grep -i "Private_Dirty:" /proc/$pid/smaps 2>/dev/null | awk '{sum += $2} END {print sum}')
    if [ -n "$dirty_pages" ] && [ "$dirty_pages" -gt 1000 ]; then
      proc_name=$(cat /proc/$pid/comm 2>/dev/null)
      dirty_kb=$((dirty_pages * 4))
      echo "PID: $pid, Name: $proc_name, Dirty Memory: $dirty_kb KB"
    fi
  fi
done | sort -k6 -nr | head -10
echo ""

echo "5. Memory Pressure (PSI):"
echo "---------------------------"
if [ -f /proc/pressure/memory ]; then
  cat /proc/pressure/memory
else
  echo "Memory pressure information is not supported in this kernel version."
fi
echo ""
