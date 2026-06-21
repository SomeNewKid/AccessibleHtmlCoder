"""LangGraph workflow for creating and reviewing an HTML document."""

from __future__ import annotations

from typing import Literal, cast

from langgraph.graph import END, StateGraph

from accessible_html_coder.coder import create_html_document
from accessible_html_coder.models import AccessibilityFinding
from accessible_html_coder.reviewer import review_html
from accessible_html_coder.state import HtmlCoderState


def build_html_coder_graph():
    """Builds the HTML coder feedback graph."""

    graph = StateGraph(HtmlCoderState)

    graph.add_node("coder", _run_coder)
    graph.add_node("reviewer", _run_reviewer)

    graph.set_entry_point("coder")
    graph.add_edge("coder", "reviewer")
    graph.add_conditional_edges(
        "reviewer", _decide_next_step, {"coder": "coder", "end": END}
    )

    return graph.compile()


def run_html_coder_graph(
    goal: str,
    max_iterations: int,
) -> HtmlCoderState:
    """Run the HTML coder graph until it succeeds or reaches the loop limit."""
    graph = build_html_coder_graph()

    initial_state: HtmlCoderState = {
        "goal": goal,
        "html": "",
        "findings": None,
        "iteration": 0,
        "max_iterations": max_iterations,
        "stop_reason": None,
    }

    final_state = graph.invoke(initial_state)
    return cast(HtmlCoderState, final_state)


def _run_coder(state: HtmlCoderState) -> dict[str, object]:
    coder_result = create_html_document(state["goal"], state["html"], state["findings"])

    return {
        "html": coder_result.html, 
        "iteration": state["iteration"] + 1, 
        "stop_reason": None
    }


def _run_reviewer(state: HtmlCoderState) -> dict[str, object]:
    findings = review_html(state["html"])

    stop_reason = None
    if not findings:
        stop_reason = "no_accessibility_findings"
    elif state["iteration"] >= state["max_iterations"]:
        stop_reason = "max_iterations_reached"

    if _same_findings(findings, state["findings"] or []):
        stop_reason = "findings_unchanged"

    return {"findings": findings, "stop_reason": stop_reason}


def _decide_next_step(state: HtmlCoderState) -> Literal["coder", "end"]:
    if state["stop_reason"]:
        return "end"

    return "coder"


def _same_findings(
        new_findings: list[AccessibilityFinding], 
        old_findings: list[AccessibilityFinding],
) -> bool:
    if not new_findings or not old_findings:
        return False

    new_rule_ids = [finding.rule_id for finding in new_findings]
    old_rule_ids = [finding.rule_id for finding in old_findings]
    
    return sorted(new_rule_ids) == sorted(old_rule_ids)