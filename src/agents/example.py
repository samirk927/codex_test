"""Example agent stub used to validate the project scaffold."""


def handle_prompt(prompt: str) -> str:
    """Return a canned response so tests can exercise the import path."""
    sanitized = prompt.strip() or "empty prompt"
    return f"example agent received: {sanitized}"
