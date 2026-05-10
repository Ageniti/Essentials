"""Swarm backend abstraction for teammate execution."""

from __future__ import annotations

from importlib import import_module

from essentials.swarm.registry import BackendRegistry, get_backend_registry
from essentials.swarm.subprocess_backend import SubprocessBackend
from essentials.swarm.types import (
    BackendType,
    SpawnResult,
    TeammateExecutor,
    TeammateMessage,
    TeammateSpawnConfig,
)

_LAZY_EXPORTS = {
    "MailboxMessage": ("essentials.swarm.mailbox", "MailboxMessage"),
    "TeammateMailbox": ("essentials.swarm.mailbox", "TeammateMailbox"),
    "create_idle_notification": ("essentials.swarm.mailbox", "create_idle_notification"),
    "create_shutdown_request": ("essentials.swarm.mailbox", "create_shutdown_request"),
    "create_user_message": ("essentials.swarm.mailbox", "create_user_message"),
    "get_agent_mailbox_dir": ("essentials.swarm.mailbox", "get_agent_mailbox_dir"),
    "get_team_dir": ("essentials.swarm.mailbox", "get_team_dir"),
}

__all__ = [
    "BackendRegistry",
    "BackendType",
    "MailboxMessage",
    "SpawnResult",
    "SubprocessBackend",
    "TeammateExecutor",
    "TeammateMailbox",
    "TeammateMessage",
    "TeammateSpawnConfig",
    "create_idle_notification",
    "create_shutdown_request",
    "create_user_message",
    "get_agent_mailbox_dir",
    "get_backend_registry",
    "get_team_dir",
]


def __getattr__(name: str):
    """Lazily load POSIX-only swarm helpers when they are actually used."""
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = target
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value
