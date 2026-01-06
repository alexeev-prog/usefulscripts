#!/usr/bin/env bash

set -e

DEFAULT_WATCH_DIR="."
WATCH_DIR="${1:-$DEFAULT_WATCH_DIR}"
EVENTS="create,delete,modify,moved_to,moved_from"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

declare -A EVENT_COLORS=(
    ["CREATE"]=$GREEN
    ["DELETE"]=$RED
    ["MODIFY"]=$BLUE
    ["MOVED_TO"]=$PURPLE
    ["MOVED_FROM"]=$CYAN
)

declare -A EVENT_EMOJIS=(
    ["CREATE"]="📁"
    ["DELETE"]="❌"
    ["MODIFY"]="✏️"
    ["MOVED_TO"]="➡️"
    ["MOVED_FROM"]="⬅️"
)

check_dependencies() {
    if ! command -v inotifywait &> /dev/null; then
        echo -e "${RED}Error: inotifywait is not installed.${NC}"
        exit 1
    fi
}

validate_directory() {
    if [ ! -d "$WATCH_DIR" ]; then
        echo -e "${RED}Error: Directory '$WATCH_DIR' does not exist.${NC}"
        exit 1
    fi
}

send_notification() {
    local event="$1"
    local file="$2"
    local message="$3"

    if command -v notify-send &> /dev/null; then
        notify-send "File System Event" "${EVENT_EMOJIS[$event]} $message\nFile: $file" \
            --icon=dialog-information
    fi
}

process_events() {
    inotifywait -m -r -e "$EVENTS" --format "%e %w%f" "$WATCH_DIR" | \
    while read -r event file; do
        event=${event^^}
        event=${event//, / }

        for e in $event; do
            color=${EVENT_COLORS[$e]:-$YELLOW}
            emoji=${EVENT_EMOJIS[$e]:-"⚡"}

            echo -e "${color}${emoji} [${e}] ${file}${NC}"
            send_notification "$e" "$file" "File system event detected: ${e}"
        done
    done
}

main() {
    check_dependencies
    validate_directory

    echo -e "${GREEN}👀 Watching directory: ${WATCH_DIR}${NC}"
    echo -e "${YELLOW}📝 Monitoring events: ${EVENTS}${NC}"
    echo -e "${BLUE}🚀 Press Ctrl+C to stop...${NC}"
    echo ""

    process_events
}

main
