# Quickstart

## Install

```bash
uv sync --extra dev
uv pip install -e .
```

## Launch the interactive UI

```bash
essentials
```

## Run a single prompt

```bash
essentials -p "summarize this repository"
```

## Preview runtime configuration

```bash
essentials --dry-run -p "inspect available tools"
```

## Configure authentication

Use one of the built-in auth flows:

```bash
essentials auth login
```

Or set provider credentials directly:

```bash
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
```

## Common workflow

1. Start in the repository that should be analyzed or edited.
2. Launch `essentials`.
3. Ask for research, code changes, or verification.
4. Use `--dry-run` when validating settings or tool availability.
5. Use session persistence to resume work in the same project later.
