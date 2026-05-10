# Contributing to Essentials

Thanks for contributing.

Essentials is intentionally small in scope. The project is strongest when
changes make the runtime easier to understand, easier to verify, and easier to
maintain.

## What Fits Best

Good contributions usually:

- simplify the runtime or remove dead code
- improve reliability of the core agent loop
- strengthen task, tool, permission, or session behavior
- improve documentation, examples, and repository clarity
- add focused tests or validation for real regression risk

Less likely to fit:

- adding broad product layers outside the local agent core
- introducing large compatibility shims for old behavior
- adding multiple alternate execution paths that are not clearly necessary
- expanding surface area without clear maintenance value

## Development Setup

```bash
uv sync --extra dev
uv pip install -e .
```

Useful checks:

```bash
uv run python -m compileall src/essentials src/__init__.py
uv run pytest
uv run ruff check .
```

## Pull Request Guidelines

- keep changes scoped and easy to review
- prefer small, targeted pull requests over broad rewrites
- explain the problem and the design tradeoff in the PR description
- update docs when behavior, commands, or configuration change
- avoid mixing unrelated cleanup with feature work

## Design Expectations

When in doubt, prefer:

- fewer code paths
- fewer compatibility layers
- explicit behavior over clever indirection
- direct local workflows over product-style abstraction

If a feature makes the repository feel heavier, more ambiguous, or harder to
verify, it is probably the wrong direction for Essentials.
