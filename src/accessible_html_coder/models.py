"""Models."""

from __future__ import annotations

from pydantic import BaseModel


class AccessibilityFinding(BaseModel):
    """An accessibility issue found in an HTML document."""

    rule_id: str
    impact: str
    description: str
    help_text: str
    target: list[str]
    failure_summary: str


class CoderResult(BaseModel):
    """The results of the coder."""

    html: str
    notes: str
