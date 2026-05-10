# Providers

Essentials currently supports two practical provider paths:

- Anthropic
- OpenAI-compatible APIs

The runtime intentionally avoids a large matrix of provider-specific behavior.

## Anthropic

Use Anthropic by setting an Anthropic model and API key:

```bash
export ANTHROPIC_API_KEY=...
essentials
```

Typical model examples:

- `claude-3-7-sonnet-latest`
- `claude-sonnet-4-0`

## OpenAI-compatible

Use any API that follows the OpenAI-compatible chat interface by configuring:

- model name
- API key
- base URL

Example:

```bash
export OPENAI_API_KEY=...
```

```json
{
  "provider": "openai",
  "model": "gpt-4.1",
  "base_url": "https://api.openai.com/v1"
}
```

This same path can be used for compatible third-party endpoints as long as they
behave closely enough to the expected chat-completions interface.

## Choosing a provider

Anthropic is usually the simplest option when using Claude models directly.

OpenAI-compatible mode is the right fit when using:

- OpenAI
- OpenRouter
- self-hosted compatible gateways
- vendor APIs that intentionally mirror the OpenAI interface

## Notes

- Essentials does not try to maintain broad compatibility shims for every edge
  case across every provider.
- Simpler provider behavior is preferred over a large compatibility surface.
