#!/usr/bin/env python3
import argparse
import json
import logging
import os
from collections.abc import Iterable
from pathlib import Path

logging.basicConfig(
    filename=".file_sorter.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    encoding="utf-8",
)

logging.getLogger().addHandler(logging.StreamHandler())


__author__ = "alexeev-prog"
__version__ = "v0.1.0"

DEFAULT_EXTENSIONS = {
    "Documents": {
        "exts": (".pdf", ".docx", ".doc", ".odt", ".rtf", ".wps"),
        "directory_name": "documents",
    },
    "Images": {
        "exts": (
            ".png",
            ".svg",
            ".webp",
            ".jpeg",
            ".jpg",
            ".gif",
            ".bmp",
            ".tif",
            ".tiff",
            ".raw",
            ".ico",
            ".jfif",
            ".heic",
        ),
        "directory_name": "images",
    },
    "Archives": {
        "exts": (
            ".xz",
            ".bz",
            ".tar",
            ".zip",
            ".rar",
            ".7z",
            ".gz",
            ".lzip",
            ".cab",
            ".iso",
            ".dmg",
        ),
        "directory_name": "archives",
    },
    "Text": {
        "exts": (".md", ".rst", ".json", ".log", ".sql"),
        "directory_name": "text",
    },
    "Books": {
        "exts": (".fb2", ".epub", ".mobi", ".azw", ".azw3"),
        "directory_name": "books",
    },
    "Spreadsheet": {
        "exts": (".xlsx", ".xls", ".xlsm", ".ods", ".xltx", ".csv"),
        "directory_name": "spreadsheets",
    },
    "Videos": {
        "exts": (
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
            ".wmv",
            ".mpg",
            ".mpeg",
            ".m4v",
            ".webm",
            ".flv",
            ".3gp",
            ".rmvb",
        ),
        "directory_name": "videos",
    },
    "Audios": {
        "exts": (
            ".mp3",
            ".wav",
            ".ogg",
            ".flac",
            ".aif",
            ".mid",
            ".midi",
            ".wma",
            ".aac",
            ".m4a",
            ".opus",
            ".ape",
            ".dsd",
        ),
        "directory_name": "audios",
    },
    "Java": {"exts": (".java", ".jar", ".class", ".javadoc"), "directory_name": "java"},
    "Scripts": {
        "exts": (
            ".sh",
            ".bash",
            ".bat",
            ".fish",
            ".zsh",
            ".ps",
            ".py",
            ".rb",
            ".pl",
            ".lua",
            ".jsp",
        ),
        "directory_name": "scripts",
    },
    "Garbage": {
        "exts": (".crdownload", ".flatpakref", ".part", ".tmp", ".swp"),
        "directory_name": ".garbage",
    },
    "3D Models": {
        "exts": (".fbx", ".obj", ".stl", ".3ds", ".blend", ".dae", ".ply", ".svgz"),
        "directory_name": "3d_models",
    },
    "Configuration": {
        "exts": (
            ".cfg",
            ".conf",
            ".properties",
            ".ini",
            ".yaml",
            ".toml",
            ".yml",
            ".config",
        ),
        "directory_name": "configurations",
    },
    "Fonts": {
        "exts": (".ttf", ".otf", ".woff", ".woff2", ".eot"),
        "directory_name": "fonts",
    },
    "Web": {
        "exts": (".html", ".htm", ".css", ".js", ".ts", ".php"),
        "directory_name": "web",
    },
    "Virtual Machines": {
        "exts": (".vmdk", ".vdi", ".ova", ".ovf", ".box"),
        "directory_name": "virtual_machines",
    },
    "Presentations": {
        "exts": (".ppt", ".pptx", ".key", ".odp"),
        "directory_name": "presentations",
    },
    "OpenVPN": {"exts": (".ovpn", ".openvpn"), "directory_name": "openvpn"},
}


def load_extensions(filename: str = "extensions.json"):
    if Path(filename).exists():
        with open(filename) as read_file:
            data = json.load(read_file)
    else:
        with open(filename, "w") as write_file:
            json.dump(DEFAULT_EXTENSIONS, write_file, indent=4)
        data = DEFAULT_EXTENSIONS

    return data


EXTENSIONS = load_extensions()


class Folder:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path) if isinstance(path, str) else path

    def _get_subfolder_paths(self) -> Iterable:
        return (folder.path for folder in os.scandir(self.path) if folder.is_dir())

    def _get_file_paths(self) -> Iterable:
        return (file.path for file in os.scandir(self.path) if not file.is_dir())

    def _create_subfolder(self, subfolder_name: str) -> None:
        subfolder_path = self.path / subfolder_name

        if not subfolder_path.exists():
            subfolder_path.mkdir()

    def sort_files_by_extensions(self) -> None:
        for name, ext_data in EXTENSIONS.items():
            for filepath in self._get_file_paths():
                path = Path(filepath)
                extension = path.suffix

                if extension in ext_data["exts"] or "*" in ext_data["exts"]:
                    subfolder_name = Path(ext_data["directory_name"])
                    self._create_subfolder(subfolder_name)

                    try:
                        new_path = Path(self.path, subfolder_name, path.name)
                        logging.info(
                            f"[{name}] {path.name} -> {'/'.join(new_path.parts[-2:])}"
                        )
                        path.rename(new_path)
                    except Exception as ex:
                        logging.exception(
                            f"Error raised when working with {self.path}: {ex}"
                        )


def main():
    print(f"DD-cleaner (C) {__author__} {__version__}")

    parser = argparse.ArgumentParser(description="Sorting files by extensions")
    parser.add_argument(
        "--dir",
        type=str,
        help="Input dir for sorting",
        default=f"{os.getenv('HOME')}/Downloads",
    )

    args = parser.parse_args()

    folder_path = args.dir

    folder = Folder(folder_path)

    logging.info(f"Sorting files by extensions in {folder_path}")
    print()
    folder.sort_files_by_extensions()


if __name__ == "__main__":
    main()
