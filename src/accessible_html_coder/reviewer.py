"""Reviews accessibility of an HTML web page."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from accessible_html_coder.models import AccessibilityFinding


def review_html(html: str) -> list[AccessibilityFinding]:
    """Run axe-core against an HTML document and return accessibility findings."""
    axe_script_path = _get_axe_script_path()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        try:
            page.set_content(html, wait_until="load")
            page.add_script_tag(path=str(axe_script_path))

            axe_result = page.evaluate(
                """
                async () => { return await axe.run(document) }
                """
            )
        finally:
            browser.close()

    return _parse_axe_result(axe_result)


def _get_axe_script_path() -> Path:
    axe_script_path = Path.cwd() / "node_modules" / "axe-core" / "axe.min.js"

    if not axe_script_path.exists():
        raise ValueError(
            "Could not find axe-core. Run this from the project root first: "
            "npm install axe-core --save-dev"
        )

    return axe_script_path


def _parse_axe_result(axe_result: dict[str, Any]) -> list[AccessibilityFinding]:
    findings: list[AccessibilityFinding] = []

    violations = axe_result.get("violations", [])
    for violation in violations:
        nodes = violation.get("nodes", [])

        for node in nodes:
            finding = AccessibilityFinding(
                rule_id=violation.get("id", ""),
                impact=violation.get("impact", ""),
                description=violation.get("description", ""),
                help_text=violation.get("help", ""),
                target=node.get("target", []),
                failure_summary=node.get("failureSummary", ""),
            )
            findings.append(finding)

    return findings
