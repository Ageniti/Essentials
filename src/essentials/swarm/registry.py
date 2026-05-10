"""Backend registry for teammate execution."""

from __future__ import annotations

import logging
from essentials.swarm.types import BackendType, TeammateExecutor

logger = logging.getLogger(__name__)


class BackendRegistry:
    """Registry that maps BackendType names to TeammateExecutor instances.
    """

    def __init__(self) -> None:
        self._backends: dict[BackendType, TeammateExecutor] = {}
        self._detected: BackendType | None = None
        self._register_defaults()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_backend(self, executor: TeammateExecutor) -> None:
        """Register a custom executor under its declared ``type`` key."""
        self._backends[executor.type] = executor
        logger.debug("Registered backend: %s", executor.type)

    def detect_backend(self) -> BackendType:
        """Return the only supported backend type."""
        if self._detected is not None:
            return self._detected
        self._detected = "subprocess"
        return self._detected

    def get_executor(self, backend: BackendType | None = None) -> TeammateExecutor:
        """Return a TeammateExecutor for the given backend type.

        Args:
            backend: Explicit backend type to use. When *None* the registry
                     auto-detects the best available backend.

        Returns:
            The registered :class:`~essentials.swarm.types.TeammateExecutor`.

        Raises:
            KeyError: If the requested backend has not been registered.
        """
        resolved = backend or self.detect_backend()
        executor = self._backends.get(resolved)
        if executor is None:
            available = list(self._backends.keys())
            raise KeyError(
                f"Backend {resolved!r} is not registered. Available: {available}"
            )
        return executor

    def available_backends(self) -> list[BackendType]:
        """Return sorted list of registered backend types."""
        return sorted(self._backends.keys())  # type: ignore[return-value]

    def reset(self) -> None:
        """Clear detection cache and re-register defaults.

        Intended for testing — allows re-detection after env changes.
        """
        self._detected = None
        self._backends.clear()
        self._register_defaults()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _register_defaults(self) -> None:
        """Register built-in backends."""
        from essentials.swarm.subprocess_backend import SubprocessBackend

        self._backends["subprocess"] = SubprocessBackend()


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_registry: BackendRegistry | None = None


def get_backend_registry() -> BackendRegistry:
    """Return the process-wide singleton BackendRegistry."""
    global _registry
    if _registry is None:
        _registry = BackendRegistry()
    return _registry
