"""API error types for Essentials."""

from __future__ import annotations


class EssentialsApiError(RuntimeError):
    """Base class for upstream API failures."""


class AuthenticationFailure(EssentialsApiError):
    """Raised when the upstream service rejects the provided credentials."""


class RateLimitFailure(EssentialsApiError):
    """Raised when the upstream service rejects the request due to rate limits."""


class RequestFailure(EssentialsApiError):
    """Raised for generic request or transport failures."""
