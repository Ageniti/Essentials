# Architecture

Essentials is organized as a compact local-first agent runtime.

## Main layers

- `config`: settings, local paths, and provider profiles
- `api`: model client implementations and provider detection
- `engine`: conversation loop, tool orchestration, and streaming response flow
- `tools`: file, shell, search, MCP, task, and utility tools
- `tasks`: local background task management
- `swarm`: subprocess-based worker agent execution
- `memory`: project-level persistent memory
- `services`: session storage, compaction, cron, token estimation, and LSP helpers
- `ui`: runtime assembly and Textual interface

## Execution model

The default execution path is intentionally simple:

1. The main runtime builds settings, tools, hooks, MCP, and prompt context.
2. The query engine streams model output and dispatches tool calls.
3. Tools interact with the repository, shell, background tasks, or MCP servers.
4. Optional worker agents are launched as subprocess-backed tasks.
5. Session snapshots and compaction keep long-running work manageable.

## Design constraints

Essentials prefers:

- a small number of real execution paths
- local-first operation
- explicit configuration
- inspectable source over opaque abstractions
- reduced product surface outside the core agent workflow
