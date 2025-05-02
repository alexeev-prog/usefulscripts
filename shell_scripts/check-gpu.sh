#!/usr/bin/env bash

gpu_info=$(lspci | grep -i 'vga\|3d\|2d')

if [[ $gpu_info == *"AMD"* ]]; then
	echo "AMD GPU"
elif [[  $gpu_info == *"Intel"*  ]]; then
	echo "Intel GPU"
else
	echo "Unknown GPU"
fi
