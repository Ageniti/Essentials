"""Shared utilities for spawning teammate processes."""

from __future__ import annotations

import os
import shutil
import sys


# Environment variable to override the teammate command
TEAMMATE_COMMAND_ENV_VAR = "ESSENTIALS_TEAMMATE_COMMAND"


# ---------------------------------------------------------------------------
# Environment variables forwarded to spawned teammates.
#
# Spawned teammates should inherit the leader's provider and config env vars.
# ---------------------------------------------------------------------------

_TEAMMATE_ENV_VARS = [
    # --- API provider selection -------------------------------------------
    # Without these, teammates would default to the wrong endpoint provider
    # and fail all API calls (analogous to GitHub issue #23561 in the TS source).
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
    # --- Config directory override ----------------------------------------
    # Allows operator-level config to be visible inside teammate processes.
    "CLAUDE_CONFIG_DIR",
    # --- Remote / CCR markers ---------------------------------------------
    # CCR-aware code paths check CLAUDE_CODE_REMOTE.  Auth finds its own
    # way; the FD env var wouldn't help across tmux boundaries anyway.
    "CLAUDE_CODE_REMOTE",
    # Auto-memory gate checks REMOTE && !MEMORY_DIR to disable memory on
    # ephemeral CCR filesystems.  Forwarding REMOTE alone would flip
    # teammates to memory-off when the parent has it on.
    "CLAUDE_CODE_REMOTE_MEMORY_DIR",
    # --- Upstream proxy settings ------------------------------------------
    # The parent's MITM relay is reachable from teammates on the same
    # container network.  Forward proxy vars so teammates route
    # customer-configured traffic through the relay for credential injection.
    # Without these, teammates bypass the proxy entirely.
    "HTTPS_PROXY",
    "https_proxy",
    "HTTP_PROXY",
    "http_proxy",
    "NO_PROXY",
    "no_proxy",
    # --- CA bundle overrides ----------------------------------------------
    # Custom CA certificates must be visible to teammates when TLS inspection
    # is in use; missing these causes SSL verification failures.
    "SSL_CERT_FILE",
    "NODE_EXTRA_CA_CERTS",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    # --- Essentials-native provider settings --------------------------------
    # These are read by settings._apply_env_overrides().
    "ESSENTIALS_API_FORMAT",
    "ESSENTIALS_BASE_URL",
    "ESSENTIALS_MODEL",
    "ESSENTIALS_CONFIG_DIR",
    "ESSENTIALS_DATA_DIR",
    "ESSENTIALS_LOGS_DIR",
    "OPENAI_API_KEY",
]


def get_teammate_command() -> str:
    """Return the executable used to spawn teammate processes.

    Resolution order:
    1. ``ESSENTIALS_TEAMMATE_COMMAND`` environment variable — allows the
       operator to point at a specific binary or wrapper script.
    2. The current Python interpreter running the ``essentials`` module.
       This keeps spawned teammates on the same venv/source tree as the
       leader process.
    3. The ``essentials`` entry-point on PATH (installed package fallback).
    """
    override = os.environ.get(TEAMMATE_COMMAND_ENV_VAR)
    if override:
        return override

    # Prefer the current interpreter so teammates inherit the same runtime and
    # editable-install source tree as the parent process.
    if sys.executable:
        return sys.executable

    entry_point = shutil.which("essentials")
    if entry_point:
        return entry_point
    return "python"


def build_inherited_cli_flags(
    *,
    model: str | None = None,
    system_prompt: str | None = None,
    system_prompt_mode: str | None = None,
    permission_mode: str | None = None,
    plan_mode_required: bool = False,
    settings_path: str | None = None,
    extra_flags: list[str] | None = None,
) -> list[str]:
    """Build CLI flags to propagate from the current session to spawned teammates.

    Ensures teammates inherit important settings like permission mode, model
    selection, and plugin configuration from their parent.

    Args:
        model: Model override to forward (e.g. ``"claude-opus-4-6"``).
        system_prompt: System prompt override to forward to the teammate.
        system_prompt_mode: One of ``"replace"``/``"default"`` or ``"append"``.
            ``append`` maps to ``--append-system-prompt``; anything else uses
            ``--system-prompt``.
        permission_mode: One of the current permission mode values.
        plan_mode_required: When True, bypass-permissions flag is suppressed
            (plan mode takes precedence over bypass for safety).
        settings_path: Path to a settings JSON file to propagate via
            ``--settings``.
        extra_flags: Additional pre-built flag strings to append verbatim.
            Callers are responsible for splitting these as argv tokens.

    Returns:
        List of CLI flag strings ready to be passed to :mod:`subprocess`.
    """
    flags: list[str] = []

    # --- Permission mode ---------------------------------------------------
    # Plan mode takes precedence over bypass permissions for safety.
    if plan_mode_required:
        flags.extend(["--permission-mode", "plan"])
    elif permission_mode in {"default", "plan", "full_auto"}:
        flags.extend(["--permission-mode", permission_mode])

    # --- Model override ----------------------------------------------------
    # "inherit" means use the parent's model via the ESSENTIALS_MODEL env var.
    if model and model != "inherit":
        flags.extend(["--model", model])

    # --- System prompt override ------------------------------------------
    # Agent definitions can carry a dedicated worker system prompt. Forward it
    # explicitly so subprocess teammates preserve their role/personality.
    if system_prompt:
        prompt_flag = "--append-system-prompt" if system_prompt_mode == "append" else "--system-prompt"
        flags.extend([prompt_flag, system_prompt])

    # --- Settings path propagation ----------------------------------------
    # Ensures teammates load the same settings JSON as the leader process.
    if settings_path:
        flags.extend(["--settings", settings_path])

    if extra_flags:
        flags.extend(extra_flags)

    return flags


def build_inherited_env_vars() -> dict[str, str]:
    """Build environment variables to forward to spawned teammates.

    Always includes ``ESSENTIALS_AGENT_TEAMS=1`` plus any provider/proxy
    vars that are set in the current process.

    Returns:
        Dict of env var name → value to merge into the subprocess environment.
    """
    env: dict[str, str] = {
        "ESSENTIALS_AGENT_TEAMS": "1",
        "CLAUDE_CODE_COORDINATOR_MODE": "0",
    }

    for key in _TEAMMATE_ENV_VARS:
        value = os.environ.get(key)
        if value:
            env[key] = value

    return env
