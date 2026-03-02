# Repository Guidelines

## Project Structure & Module Organization
- Core package lives in `vt2pbf/`.
- Public entry points are in `vt2pbf/__init__.py` and `vt2pbf/encoder.py`.
- Encoding internals are under `vt2pbf/service/` (`feature.py`, `layer.py`, `tile.py`).
- Protobuf bindings and schema are in `vt2pbf/mapbox/` (`vector_tile.proto`, versioned `protobuf_3` ... `protobuf_7` modules).
- Tests live in `tests/` with shared fixtures/helpers in `tests/data.py`.

## Build, Test, and Development Commands
- Install editable package + dev tools:
  - `uv pip install -e .[dev]`
- Lint and auto-fix:
  - `make lint` (runs `ruff format` + `ruff check --fix`)
- Lint without formatting:
  - `make lint-no-format`
- Run tests:
  - `make test` or `uv run pytest -q`
- Build distributions:
  - `uv build` (produces wheel/sdist in `dist/`)

## Coding Style & Naming Conventions
- Python style is enforced by Ruff (`pyproject.toml`):
  - 4-space indentation, max line length `120`, single quotes, sorted imports.
- Use `snake_case` for modules, functions, variables, and test files.
- Keep package API additions explicit in `vt2pbf/__init__.py`.
- Do not manually edit generated protobuf Python files unless you are intentionally regenerating bindings.

## Testing Guidelines
- Framework: `pytest`.
- Test files should follow `test_*.py`; test names should start with `test_`.
- Add/adjust tests in `tests/` for every behavior change, especially around geometry/tag encoding edge cases.
- CI validates across Python `3.9`-`3.14` and protobuf majors `3`-`7`; avoid changes tied to one protobuf major.

## Commit & Pull Request Guidelines
- Follow existing history style: short imperative subject lines (examples: `Add support for protobuf 5 and 6`, `CI: switch to ubuntu-latest...`).
- Keep commits focused and logically grouped.
- Every newly created file **must** be added to Git (`git add <path>`) in the same branch/session to avoid losing untracked work.
- PRs should include:
  - clear problem/solution summary,
  - linked issue (if any),
  - tests run locally (commands + result),
  - notes on compatibility impact (Python/protobuf versions).
- If behavior/output changes, include before/after snippets in the PR description.
