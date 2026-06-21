"""State management."""

from __future__ import annotations

from typing import TypedDict

from accessible_html_coder.models import AccessibilityFinding


class HtmlCoderState(TypedDict):
    """State for the HTML coder."""

    goal: str
    html: str
    findings: list[AccessibilityFinding] | None
    iteration: int
    max_iterations: int
    stop_reason: str | None
