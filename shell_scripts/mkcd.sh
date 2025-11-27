#!/usr/bin/env bash

mkcd() {
    if [[ $# -eq 0 ]]; then
        echo -e "\033[1;31mError: Directory name required\033[0m" >&2
        echo -e "\033[1;33mUsage: mkcd <directory>\033[0m" >&2
        return 1
    fi

    local dir="$1"

    if \mkdir -p "$dir"; then
        if cd "$dir"; then
            echo -e "\033[1;32mCreated and entered: $(pwd)\033[0m"
        else
            echo -e "\033[1;31mError: Cannot enter directory: $dir\033[0m" >&2
            return 1
        fi
    else
        echo -e "\033[1;31mError: Cannot create directory: $dir\033[0m" >&2
        return 1
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    mkcd "$@"
fi
