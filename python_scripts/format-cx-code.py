import argparse
import os
import subprocess

count = 0


def find_source_files(root_dir, ignore_dirs):
    source_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove ignored directories from dirnames to prevent walking into them
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            if filename.endswith((".c", ".cpp", ".h", ".hpp", ".cc", ".cxx", ".hh")):
                source_files.append(os.path.join(dirpath, filename))
    return source_files


def format_files(files, clang_format, style):
    global count

    for file in files:
        try:
            cmd = [clang_format, "-i", "--style", style, file]
            subprocess.run(cmd, check=True)
            print(f"\033[32mFormatted:\033[0m {file}")
            count += 1
        except subprocess.CalledProcessError as e:
            print(f"\033[31mError formatting {file}:\033[0m {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Recursively format C/C++ files with clang-format"
    )
    parser.add_argument("root_dir", help="Root directory to search for source files")
    parser.add_argument("--ignore", nargs="+", default=[], help="Directories to ignore")
    parser.add_argument(
        "--clang-format", default="clang-format", help="Path to clang-format executable"
    )
    parser.add_argument(
        "--style", default="file", help="Formatting style (file/Google/LLVM/etc.)"
    )

    args = parser.parse_args()

    print("\033[36m=== C/C++ Source Formatter ===\033[0m")
    print(f"\033[33mRoot directory:\033[0m {args.root_dir}")
    print(f"\033[33mIgnored directories:\033[0m {args.ignore or 'None'}")
    print(f"\033[33mStyle:\033[0m {args.style}")
    print("\033[36m" + "=" * 30 + "\033[0m")

    source_files = find_source_files(args.root_dir, args.ignore)

    if not source_files:
        print("\033[33mNo C/C++ files found to format.\033[0m")
        return

    print(f"\033[33mFound {len(source_files)} files to format:\033[0m")
    format_files(source_files, args.clang_format, args.style)
    print(f"\033[32mFormatting complete ({count} files)!\033[0m")


if __name__ == "__main__":
    main()
