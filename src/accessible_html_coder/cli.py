"""Command-line interface for the application."""

from __future__ import annotations

import sys
from pathlib import Path

from accessible_html_coder.files import read_file, save_file
from accessible_html_coder.graph import run_html_coder_graph

MAX_ITERATIONS = 5


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    requirements_file_name = _get_requirements_file_name(argv)
    if not requirements_file_name:
        example = "the-big-lebowski.txt"
        raise SystemExit(f'Usage: python -m accessible_html_coder "{example}"')

    html_document_file = Path(requirements_file_name).with_suffix(".html")
    html_document_file_name = html_document_file.name
    if html_document_file.exists():
        html_document_file.unlink()

    requirements = read_file(requirements_file_name)

    final_state = run_html_coder_graph(goal=requirements, max_iterations=MAX_ITERATIONS)

    generated_html = final_state["html"]

    saved_file: Path = save_file(html_document_file_name, generated_html)
    if saved_file.exists():
        print("Created file:", saved_file.name)
    else:
        print("No file created.")
    print("Iterations:", final_state["iteration"])
    print("Stop reason:", final_state["stop_reason"])
    remaining_findings = final_state["findings"]
    if remaining_findings:
        print("Remaining findings:", len(remaining_findings))

    return 0


def _get_requirements_file_name(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return args[0]
