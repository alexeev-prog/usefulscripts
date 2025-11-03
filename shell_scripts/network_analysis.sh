#!/usr/bin/env bash

echo "=== Network Connections and Traffic Analysis ==="
echo "Timestamp: $(date)"
echo ""

echo "1. Network Interface Statistics:"
echo "------------------------------------"
if command -v ip &> /dev/null; then
  ip -s link
else
  netstat -i
fi
echo ""

echo "2. Connection Count by State:"
echo "--------------------------------------"
netstat -tun | awk '/^tcp/ {state[$6]++} END {
  for (s in state) print s, state[s]
}' | sort -rn -k2
echo ""

echo "3. Top 10 Processes by Network Connections:"
echo "---------------------------------------------------"
netstat -tunp 2>/dev/null | awk '$6=="ESTABLISHED"{print $7}' | cut -d'/' -f1 | sort | uniq -c | sort -rn | head -10 | while read count pid; do
  if [ -n "$pid" ] && [ "$pid" != "-" ]; then
    proc_name=$(ps -p $pid -o comm= 2>/dev/null)
    echo "Connections: $count, PID: $pid, Process: $proc_name"
  fi
done
echo ""

echo "4. Listening Ports (excluding standard 22, 80, 443, 5432, etc.):"
echo "------------------------------------------------------------------"
netstat -tunlp | grep LISTEN | while read line; do
  port=$(echo $line | awk '{print $4}' | awk -F: '{print $NF}')
  pid_program=$(echo $line | awk '{print $7}')
  if [[ "$port" =~ ^(22|80|443|53|25|587|993|995|5432|3306|27017|11211|6379)$ ]]; then
    continue
  fi
  pid=$(echo $pid_program | cut -d'/' -f1)
  program=$(echo $pid_program | cut -d'/' -f2-)
  echo "Port: $port, PID: $pid, Process: $program"
done
echo ""

echo "5. Network Error and Drop Statistics:"
echo "---------------------------------------"
if command -v ip &> /dev/null; then
  echo "Interface    | Errors(RX/TX) | Drops(RX/TX)"
  echo "-------------|---------------|--------------"
  ip -s link show | awk '
    /^[0-9]+:/ {iface=$2; getline}
    /RX.*bytes/ {getline; rx_err=$2; tx_err=$10; getline; rx_drop=$2; tx_drop=$10; 
    printf "%-12s | %-13s | %-12s\n", iface, rx_err"/"tx_err, rx_drop"/"tx_drop}'
else
  netstat -i | awk 'NR>2 {print $1, $5"/"$9, $6"/"$10}'
fi
