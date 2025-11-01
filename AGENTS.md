# Repository Guidelines

## Project Structure & Module Organization
The repository currently starts as a clean slate; use the following layout to keep contributions predictable. Place production code under `src/`, grouping agents in `src/agents/<agent_name>.py` and shared helpers in `src/shared/`. Store reproducible assets such as prompts or fixtures in `resources/` and keep experiments in `playground/`. Mirror the production layout inside `tests/` so every module has a sibling test module (for example, `src/agents/retriever.py` pairs with `tests/agents/test_retriever.py`). Keep configuration entry points (`pyproject.toml`, `.env.example`, `ruff.toml`) at the repository root.

## Build, Test, and Development Commands
Create an isolated environment with `python -m venv .venv` followed by `source .venv/bin/activate`. Install dependencies using `pip install -r requirements.txt` once that manifest exists. Run local experiments via `python -m src.agents.<agent_name>` to execute an agent entry point. Execute the automated suite with `pytest`, adding `-k "pattern"` for targeted runs, and check style with `ruff check .`. Apply formatting fixes using `black src tests` after code changes.

## Coding Style & Naming Conventions
Adopt PEP 8 defaults: four-space indentation, snake_case for variables/functions, PascalCase classes, and SCREAMING_SNAKE_CASE constants. Keep modules focused on one responsibility and prefer pure functions for testable logic. Order imports with `ruff --fix` and keep line length at or below 100 characters. Document agent behavior and side effects with concise docstrings. Generated datasets in `resources/` must include a README with reproduction steps before committing.

## Testing Guidelines
Name tests after observable behavior (e.g., `test_agent_handles_invalid_prompt`). Provide fixtures and fakes in `tests/conftest.py` for shared setup, and avoid hitting external services—use stubs instead. Add at least one happy-path and one failure-path test for every new capability. Keep coverage meaningful by exercising decision-making branches and tool integrations; file an issue if gaps must be deferred.

## Commit & Pull Request Guidelines
With no history yet, establish Conventional Commits immediately (e.g., `feat(router): add dispatcher loop`). Keep commits small, self-contained, and accompanied by passing tests. Pull requests must describe intent, highlight non-obvious decisions, note any follow-up work, and link tracking issues. Attach relevant logs or transcripts when behavior is hard to infer. Re-run checks after feedback and confirm there are no stray debug prints before requesting review.

## Security & Configuration Tips
Never commit secrets; placeholder values belong in `.env.example`. When introducing new third-party services, update `docs/integrations.md` with setup notes and validation steps so future automated agents can reproduce the flow.
