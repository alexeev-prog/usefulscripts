#!/usr/bin/env bash

tempe() {
    local temp_dir
    local subdir=""

    temp_dir=$(mktemp -d)
    if [[ $? -ne 0 ]]; then
        echo -e "\033[1;31mError: Cannot create temp directory\033[0m" >&2
        return 1
    fi

    if ! chmod -R 0700 "$temp_dir"; then№
        echo -e "\033[1;31mError: Cannot set permissions\033[0m" >&2
        return 1
    fi

    if [[ $# -eq 1 ]]; then
        subdir="$1"
        local full_path="${temp_dir}/${subdir}"

        if ! \mkdir -p "$full_path"; then
            echo -e "\033[1;31mError: Cannot create subdirectory: $subdir\033[0m" >&2
            return 1
        fi

        if ! chmod -R 0700 "$full_path"; then
            echo -e "\033[1;31mError: Cannot set subdirectory permissions\033[0m" >&2
            return 1
        fi

        if cd "$full_path"; then
            echo -e "\033[1;32mTemp directory: $(pwd)\033[0m"
        else
            echo -e "\033[1;31mError: Cannot enter directory: $full_path\033[0m" >&2
            return 1
        fi
    else
        if cd "$temp_dir"; then
            echo -e "\033[1;32mTemp directory: $(pwd)\033[0m"
        else
            echo -e "\033[1;31mError: Cannot enter temp directory: $temp_dir\033[0m" >&2
            return 1
        fi
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    tempe "$@"
fi
