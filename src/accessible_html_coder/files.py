"""Provides file operations."""

from __future__ import annotations

from pathlib import Path


def read_file(file_name: str) -> str:
    files_directory = Path.cwd() / "files"
    file_location = files_directory / file_name

    if not file_location.exists():
        raise ValueError(f"The file does not exist: {file_name}")

    return file_location.read_text()


def save_file(file_name: str, file_contents: str) -> Path:
    files_directory = Path.cwd() / "files"
    if not files_directory.exists():
        files_directory.mkdir(parents=True, exist_ok=True)

    file_location = files_directory / file_name
    file_location.write_text(file_contents)
    return file_location
