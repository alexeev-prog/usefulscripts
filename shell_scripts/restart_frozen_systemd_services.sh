#!/usr/bin/env bash

SERVICES=("nginx" "postgresql")
LOG_FILE="/var/log/systemd_healthcheck.log"

echo "🔍 Check services status... $(date)" | tee -a $LOG_FILE

for svc in "${SERVICES[@]}"; do
    systemctl is-active --quiet "$svc"
    STATUS=$?

    if [ $STATUS -ne 0 ]; then
        echo "❌ Service $svc does not worked. Restart him..." | tee -a $LOG_FILE
        systemctl restart "$svc"
        sleep 1
        systemctl is-active --quiet "$svc" && echo "✅ $svc started now." | tee -a $LOG_FILE
    else
        echo "✔️ $svc is worked." | tee -a $LOG_FILE
    fi
done
