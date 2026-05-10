<p align="center">
  <img src="./logo.svg" alt="Essentials logo" width="132" />
</p>

<h1 align="center">Essentials</h1>

<p align="center">
  A local-first coding agent runtime for terminal workflows.
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-black" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-black" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/runtime-local--first-black" alt="Local-first runtime" />
</p>

Essentials is a local-first coding agent CLI for terminal workflows. It keeps the
core pieces needed for a serious agent runtime, without the extra product
surface:

- interactive terminal agent with a Textual UI
- single-shot `--print` and `--dry-run` execution modes
- built-in file, shell, search, task, and MCP tools
- background worker agents via a simple subprocess-based swarm path
- project memory, session persistence, and automatic conversation compaction
- provider profiles for Anthropic and OpenAI-compatible backends

The project is intentionally opinionated: it favors a smaller, inspectable
agent core over a large platform surface full of half-used integrations.

## Table of Contents

- [Highlights](#highlights)
- [Project Status](#project-status)
- [Installation](#installation)
- [Authentication and Providers](#authentication-and-providers)
- [What It Does](#what-it-does)
- [Configuration](#configuration)
- [Repository Layout](#repository-layout)
- [Development](#development)
- [Documentation](#documentation)
- [Examples](#examples)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [Security](#security)
- [Code of Conduct](#code-of-conduct)
- [Lineage and Attribution](#lineage-and-attribution)
- [Non-Goals](#non-goals)
- [License](#license)

## Highlights

- **Local-first workflow**: built for repository navigation, editing, shell
  execution, and iterative coding work on a local machine.
- **Simple execution model**: one main agent runtime plus optional background
  worker agents managed as local subprocess tasks.
- **Practical toolchain**: file read/write/edit, grep, glob, bash, MCP,
  lightweight LSP helpers, skills, todo tracking, cron jobs, and task control.
- **Long-running usability**: session snapshots, transcript export, background
  task logs, and automatic context compaction for long conversations.
- **Configurable runtime**: JSON settings, provider profiles, permissions,
  hooks, plugins, and MCP server definitions.

## Project Status

Essentials is a trimmed general agent core. It intentionally excludes the
broader product layers that often accumulate around agent systems, such as
dashboards, channel gateways, frontends, or product-specific orchestration
surfaces.

If the goal is a compact, hackable local agent runtime, that constraint is a
feature rather than a limitation.

## Installation

### Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) recommended

### Development install

```bash
uv sync --extra dev
uv pip install -e .
```

### Launch

Start the interactive terminal UI:

```bash
essentials
```

Run one prompt and exit:

```bash
essentials -p "summarize this repository"
```

Preview the resolved runtime without executing a model turn:

```bash
essentials --dry-run -p "inspect available tools"
```

## Authentication and Providers

Essentials supports:

- Anthropic-compatible usage through the Anthropic API format
- OpenAI-compatible usage through a unified OpenAI-compatible client path

Typical setup options:

```bash
essentials auth login
```

or environment variables such as:

```bash
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
```

The runtime also supports named provider profiles in `~/.essentials/settings.json`.

## What It Does

At a high level, Essentials combines:

- **Agent runtime**: conversation loop, tool calls, permissions, hooks, and
  streaming output
- **Tooling**: shell commands, file operations, repository search, MCP tools,
  tasks, and worker-agent delegation
- **State management**: project memory, session storage, task tracking, and
  context compaction

The current swarm model is deliberately simple:

- one coordinator or main agent
- optional worker agents launched as subprocesses
- task-based follow-up via `send_message(...)`
- task output inspection via `task_output(...)`

## Configuration

Essentials reads settings from:

1. CLI flags
2. environment variables
3. `~/.essentials/settings.json`
4. built-in defaults

Typical configuration areas include:

- model and API endpoint selection
- active provider profile
- permission mode and tool allow/deny lists
- hooks and plugins
- MCP server configuration
- memory and sandbox behavior

The `--settings` flag accepts a path to a JSON settings file:

```bash
essentials --settings /path/to/settings.json
```

## Development

Install the project in editable mode with development dependencies:

```bash
uv sync --extra dev
uv pip install -e .
```

Typical local checks:

```bash
uv run python -m compileall src/essentials src/__init__.py
uv run pytest
uv run ruff check .
```

If working on the runtime itself, the most important directories are usually:

- `src/essentials/engine`
- `src/essentials/tools`
- `src/essentials/ui`
- `src/essentials/config`
- `src/essentials/tasks`
- `src/essentials/swarm`

## Documentation

- [Quickstart](./docs/quickstart.md)
- [Architecture](./docs/architecture.md)
- [Configuration](./docs/configuration.md)
- [Providers](./docs/providers.md)

## Examples

- [Basic Usage](./examples/basic-usage.md)
- [Worker Agents](./examples/worker-agents.md)

## Continuous Integration

The repository includes a basic GitHub Actions workflow for:

- dependency sync
- linting with Ruff
- bytecode compilation checks
- test execution with pytest

## Changelog

Project history is tracked in [CHANGELOG.md](./CHANGELOG.md).

## Repository Layout

```text
src/essentials/api          Provider clients, errors, and routing
src/essentials/auth         Authentication flows and credential management
src/essentials/commands     Slash command registry and command handlers
src/essentials/config       Settings, profiles, and local paths
src/essentials/coordinator  Coordinator/worker orchestration prompts and metadata
src/essentials/engine       Core agent loop, messages, and streaming query flow
src/essentials/hooks        Hook loading, execution, and hot reload support
src/essentials/mcp          MCP client integration
src/essentials/memory       Project memory loading and retrieval helpers
src/essentials/permissions  Tool permission checks and modes
src/essentials/plugins      Plugin discovery and loading
src/essentials/prompts      Runtime and system prompt assembly
src/essentials/sandbox      Sandboxed execution helpers
src/essentials/services     Compaction, session storage, cron, and LSP helpers
src/essentials/skills       Built-in skill content and loaders
src/essentials/state        Shared UI/runtime state
src/essentials/swarm        Subprocess-based worker backend
src/essentials/tasks        Background task management
src/essentials/tools        Built-in tool implementations
src/essentials/ui           Textual UI and runtime assembly
src/essentials/utils        Shared utility functions
```

## Contributing

Contributions that keep the project smaller, clearer, and more reliable are the
best fit for Essentials.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
In short:

- keep the execution model simple
- prefer removing dead paths over adding compatibility layers
- avoid broad product surface expansion unless it strengthens the core runtime
- verify code changes with focused checks before sending them for review

## Security

If a change touches credentials, permissions, sandboxing, command execution, or
file access boundaries, treat it as security-sensitive work.

Please report vulnerabilities privately as described in [SECURITY.md](./SECURITY.md).

## Code of Conduct

This project follows the guidelines in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## Lineage and Attribution

Essentials did not start from a blank slate.

- **Immediate lineage**: Essentials is the trimmed and renamed continuation of
  the earlier `OpenHarness` codebase, reduced to a smaller general-purpose
  agent core.
- **Design and implementation influence**: parts of the current runtime follow
  conventions inspired by **Claude Code**, especially around conversation
  compaction and the `SKILL.md`-style skill/plugin layout. In a few places this
  is explicitly documented in source comments, for example in the compaction
  subsystem under `src/essentials/services/compact/`.

The result is not intended to be a drop-in clone of either project. Essentials
is a smaller local agent runtime with its own reduced scope and architecture.

## Non-Goals

Essentials intentionally does **not** try to be:

- a hosted agent platform
- a browser dashboard product
- a multi-channel automation hub
- a kitchen-sink framework for every execution backend

Those layers were removed on purpose to keep the codebase smaller and easier to
reason about.

## License

This repository is distributed under the [MIT License](./LICENSE).

Because Essentials is a trimmed and renamed continuation of the earlier
`OpenHarness` codebase, the upstream MIT copyright notice is preserved in
`LICENSE`. Additional attribution and repository-lineage context are documented
in [NOTICE](./NOTICE).
