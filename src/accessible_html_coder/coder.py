"""Codes an HTML web page."""

from __future__ import annotations

from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from accessible_html_coder.models import AccessibilityFinding, CoderResult

MODEL_NAME = "gpt-4o"


def create_html_document(
    requirements: str,
    previous_html: str | None = None,
    findings: list[AccessibilityFinding] | None = None,
) -> CoderResult:
    if not previous_html:
        return _create_initial_html(requirements)
    return _revise_html(requirements, previous_html, findings or [])


def _create_initial_html(requirements: str) -> CoderResult:
    messages = [
        SystemMessage(content=_get_system_prompt()),
        HumanMessage(content=_get_initial_prompt(requirements)),
    ]

    return _invoke_coder(messages)


def _revise_html(
    requirements: str, previous_html: str, findings: list[AccessibilityFinding]
) -> CoderResult:
    messages = [
        SystemMessage(content=_get_system_prompt()),
        HumanMessage(
            content=_get_revision_prompt(
                requirements=requirements,
                previous_html=previous_html,
                findings=findings,
            )
        ),
    ]

    return _invoke_coder(messages)


def _invoke_coder(messages: list[SystemMessage | HumanMessage]) -> CoderResult:
    model = ChatOpenAI(model=MODEL_NAME, temperature=0.2)

    structured_model = model.with_structured_output(CoderResult)
    result = structured_model.invoke(messages)

    return cast(CoderResult, result)


def _get_system_prompt() -> str:
    return """
You are an expert HTML developer who creates small, static, accessible HTML
documents.

Return a complete HTML5 document. The document must be suitable for saving
directly as a .html file.

Follow these rules:
- Return only the structured response requested by the application.
- Put the complete HTML document in the html field.
- Do not wrap the HTML in Markdown code fences.
- Do not include explanations inside the HTML.
- Prefer semantic HTML elements.
""".strip()


def _get_initial_prompt(requirements: str) -> str:
    return f"""
Create a brand new static HTML document from these requirements:

{requirements}

The document should be simple and readable.
""".strip()


def _get_revision_prompt(
    requirements: str,
    previous_html: str,
    findings: list[AccessibilityFinding],
) -> str:
    formatted_findings = _format_findings(findings)

    return f"""
Revise the existing HTML document to address the accessibility findings.

Keep the original requirements in mind:

{requirements}

Existing HTML:

{previous_html}

Accessibility findings from axe-core:

{formatted_findings}

Update the HTML to address the findings where possible. Preserve the intent,
content, and requirements of the page. Avoid unnecessary rewrites.
""".strip()


def _format_findings(findings: list[AccessibilityFinding]) -> str:
    if not findings:
        return "No accessibility findings."

    formatted_items: list[str] = []

    for finding in findings:
        formatted_item = f"""
Rule ID: {finding.rule_id}
Impact: {finding.impact}
Description: {finding.description}
Help: {finding.help_text}
Target: {finding.target}
Failure summary: {finding.failure_summary}
""".strip()
        formatted_items.append(formatted_item)

    return "\n\n".join(formatted_items)
