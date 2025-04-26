#!/bin/bash

echo -e "\033[1;36m=== Температуры ===\033[0m"

# CPU
cpu_temp=$(sensors | grep -E "Core [0-9]:" | awk '{print $3}' | sed 's/+//;s/°C//' | sort -nr | head -n1)
echo -e "🔥 \033[1;32mCPU: \033[1;33m${cpu_temp}°C\033[0m"

# GPU (NVIDIA)
gpu_temp=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader 2>/dev/null || echo "N/A")
echo -e "🎮 \033[1;32mGPU: \033[1;33m${gpu_temp}°C\033[0m"
