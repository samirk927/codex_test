"""Smoke tests for the example agent scaffold."""

from src.agents.example import handle_prompt


def test_handle_prompt_reports_input():
    """The placeholder agent should surface the prompt content."""
    result = handle_prompt("  Hello  ")
    assert result == "example agent received: Hello"


def test_handle_prompt_handles_empty_input():
    """An empty prompt should yield a deterministic guard string."""
    result = handle_prompt("   ")
    assert result == "example agent received: empty prompt"
