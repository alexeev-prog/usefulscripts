#!/usr/bin/env bash

# Interval
INTERVAL=5

# WiFi Interface
WIFI_INTERFACE="wlo1"

while true; do
    clear
    echo "📶 Available Wi-Fi nets:"
    nmcli -f SSID,SIGNAL,BARS device wifi list ifname "$WIFI_INTERFACE" | sort -r -k2
    sleep $INTERVAL
done
