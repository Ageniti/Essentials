"""Swarm backend type definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Backend type literals
# ---------------------------------------------------------------------------

BackendType = Literal["subprocess"]
"""The only supported backend type."""


@dataclass
class TeammateSpawnConfig:
    """Configuration for spawning a teammate."""

    name: str
    """Human-readable teammate name (e.g. ``"researcher"``)."""

    team: str
    """Team name this teammate belongs to."""

    prompt: str
    """Initial prompt / task for the teammate."""

    cwd: str
    """Working directory for the teammate."""

    parent_session_id: str
    """Parent session ID (for transcript correlation)."""

    model: str | None = None
    """Model override for this teammate."""

    command: str | None = None
    """Optional explicit command override for subprocess-backed teammates."""

    system_prompt: str | None = None
    """System prompt resolved from workflow config."""

    system_prompt_mode: Literal["default", "replace", "append"] | None = None
    """How to apply the system prompt: replace or append to default."""

    color: str | None = None
    """Optional UI color for the teammate."""

    permissions: list[str] = field(default_factory=list)
    """Tool permissions to grant this teammate."""

    plan_mode_required: bool = False
    """Whether this teammate must enter plan mode before implementing."""


# ---------------------------------------------------------------------------
# Spawn result & messaging
# ---------------------------------------------------------------------------


@dataclass
class SpawnResult:
    """Result from spawning a teammate."""

    task_id: str
    """Task ID in the task manager."""

    agent_id: str
    """Unique agent identifier (format: agentName@teamName)."""

    backend_type: BackendType
    """The backend used to spawn this agent."""

    success: bool = True
    error: str | None = None


@dataclass
class TeammateMessage:
    """Message to send to a teammate."""

    text: str
    from_agent: str
    color: str | None = None
    timestamp: str | None = None
    summary: str | None = None


# ---------------------------------------------------------------------------
# TeammateExecutor protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class TeammateExecutor(Protocol):
    """Protocol for teammate execution backends.
    """

    type: BackendType

    def is_available(self) -> bool:
        """Check if this backend is available on the system."""
        ...

    async def spawn(self, config: TeammateSpawnConfig) -> SpawnResult:
        """Spawn a new teammate with the given configuration."""
        ...

    async def send_message(self, agent_id: str, message: TeammateMessage) -> None:
        """Send a message to a running teammate via stdin."""
        ...

    async def shutdown(self, agent_id: str, *, force: bool = False) -> bool:
        """Terminate a teammate.

        Args:
            agent_id: The agent to terminate.
            force: If True, kill immediately. If False, attempt graceful shutdown.

        Returns:
            True if the agent was terminated successfully.
        """
        ...
