# Configuration

Essentials keeps configuration intentionally simple.

## Settings file

The `--settings` flag accepts a path to a JSON settings file:

```bash
essentials --settings /path/to/settings.json
```

An example minimal configuration:

```json
{
  "model": "claude-3-7-sonnet-latest",
  "provider": "anthropic",
  "permission_mode": "default"
}
```

## Main configuration areas

Common fields include:

- `model`: default model name
- `provider`: active provider profile
- `base_url`: base URL for OpenAI-compatible APIs
- `permission_mode`: tool approval behavior
- `system_prompt`: custom system prompt override
- `mcp_servers`: MCP server definitions
- `hooks`: hook definitions

## Environment variables

This repository uses the `ESSENTIALS_*` namespace for project-specific runtime
configuration.

Examples:

```bash
export ESSENTIALS_CONFIG_DIR="$HOME/.essentials"
export ESSENTIALS_TEAMMATE_COMMAND="essentials"
```

Provider credentials still use the provider-specific variables expected by the
underlying API, such as `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.

## Permissions

Permissions control whether tools run directly or require explicit approval.

This matters most for:

- shell execution
- file writes and edits
- network access
- MCP tools

## Hooks and MCP

Hooks and MCP servers are configured through settings and loaded at runtime.

- Hooks allow actions around runtime and tool events.
- MCP extends the available tool surface through external servers.

## Practical guidance

- Keep settings explicit and minimal.
- Prefer one active provider configuration instead of many overlapping profiles.
- Use `--dry-run` to inspect runtime setup without executing work.
