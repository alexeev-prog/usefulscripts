#!/usr/bin/env bash

cpu_info=$(cat /proc/cpuinfo | grep 'vendor_id' | uniq)

if [[ $cpu_info == *"GenuineIntel"* ]]; then
	echo "Intel"
else
	echo "AMD"
fi
