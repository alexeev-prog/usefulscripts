#!/usr/bin/env bash

LOG_FILE="/var/log/boot_time.log"

echo "🕰  Analyze system startup time" | tee -a $LOG_FILE

BOOT_TIME=$(systemd-analyze)

BLAME=$(systemd-analyze blame | head -n 10)

{
    echo "⏱️ $(date)"
    echo "$BOOT_TIME"
    echo "📌 Ten most slowest services:"
    echo "$BLAME"
    echo "-----------------------------"
} >> $LOG_FILE

echo "✅ Данные сохранены." | tee -a $LOG_FILE
