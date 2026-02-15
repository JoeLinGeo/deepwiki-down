#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path


class FileAdapter:

    def _sanitize_filename(self, name: str) -> str:
        # Remove control characters
        name = re.sub(r'[\x00-\x1f]', '', name)
        # Replace characters not allowed on Windows (and generally problematic) with '-'
        name = re.sub(r'[<>:\\"/\\|\?\*]', '-', name)
        # Trim trailing dots and spaces (Windows doesn't allow names ending with them)
        name = name.rstrip(' .')
        # Collapse multiple whitespace to single space
        name = re.sub(r'\s+', ' ', name)
        return name

    def write_file(self, filepath: str, content: str) -> None:
        try:
            path = Path(filepath)

            # Sanitize the final filename to avoid invalid characters on Windows
            sanitized_name = self._sanitize_filename(path.name)
            if sanitized_name != path.name:
                path = path.with_name(sanitized_name)

            # Ensure parent directory exists
            os.makedirs(path.parent, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n--- Content saved to {path} ---")
        except IOError as e:
            print(f"Error writing to file {filepath}: {e}")
            raise

    def create_directory(self, dir_path: str) -> None:
        try:
            os.makedirs(dir_path, exist_ok=True)
        except IOError as e:
            print(f"Error creating directory {dir_path}: {e}")
            raise
