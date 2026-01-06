#!/usr/bin/env python3
import os
import sys

# Define color codes for output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
NC = "\033[0m"  # No Color
BOLD = "\033[1m"  # No Color

# File Extension filter. You can add new extension
py_extensions = (".py",)
IGNORED_DIRS = ["dist", ".git", "docs", "ignored", "venv", "resources"]

RUFF = "ruff"
SPACETABS = "./space-tabs.sh"

print(f"code-formatter: {RUFF}; Extensions: {' '.join(py_extensions)}")


def print_usage():
    """Print the usage instructions."""
    print(f"{YELLOW}Usage: convert_tabs(file_path, tab_size, conversion_type){NC}")
    print("<conversion_type>: 'spaces' or 'tabs'")


def print_error(message):
    """Print error messages."""
    print(f"{RED}Error: {message}{NC}")


def validate_positive_integer(value):
    """Validate if the value is a positive integer."""
    try:
        int_value = int(value)
        if int_value < 1:
            raise ValueError
        return int_value
    except ValueError:
        print_error("Tab size must be a positive integer.")
        return None


def file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        print_error(f"File not found: {file_path}")
        return False
    return True


def main():
    os.system("isort .")
    os.system("black .")

    if len(sys.argv) > 1:
        print(f"{BOLD}Format {sys.argv[1]}{NC}")
        os.system(f"{RUFF} check {sys.argv[1]} --fix")
        os.system(f"{RUFF} format {sys.argv[1]}")
        print(f"{GREEN}Formatting completed successfully: {sys.argv[1]}{NC}")
        return

    for root, _dirs, files in os.walk(os.getcwd()):
        if len(set(root.split("/")).intersection(IGNORED_DIRS)) > 0:
            continue
        for file in files:
            if file.endswith(py_extensions):
                print(f"{BOLD}Format {file}: {root}/{file}{NC}")
                os.system(f"{RUFF} check {root}/{file} --fix")
                os.system(f"{RUFF} format {root}/{file}")
                print(f"{GREEN}Formatting completed successfully: {root}/{file}{NC}")

    os.system("ruff clean")


if __name__ == "__main__":
    main()
