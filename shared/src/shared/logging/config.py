"""Configuration and factories for project-wide structured logging."""

from __future__ import annotations

import logging
import sys
from threading import Lock
from typing import cast

import structlog
from structlog.typing import EventDict

_configuration_lock = Lock()
_is_configured = False


def configure_logging(*, level: str | int = "INFO", json_logs: bool = False) -> None:
    """Configure structured logging for the current process.

    Args:
        level: Minimum log level as a standard logging level name or integer.
        json_logs: Emit JSON when true; otherwise emit human-readable console logs.

    Raises:
        ValueError: If ``level`` is not a valid standard logging level.
    """
    global _is_configured

    log_level = _resolve_log_level(level)
    renderer = (
        structlog.processors.JSONRenderer()
        if json_logs
        else structlog.dev.ConsoleRenderer(colors=False)
    )

    with _configuration_lock:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                renderer,
            ],
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            cache_logger_on_first_use=False,
        )
        _is_configured = True


def get_logger(name: str) -> structlog.BoundLogger:
    """Return a project logger, configuring console logging on first use."""
    if not _is_configured:
        configure_logging()

    return structlog.get_logger(name)


def bind_context(**context: object) -> None:
    """Bind request-scoped fields, such as ``correlation_id``, to future logs."""
    structlog.contextvars.bind_contextvars(**cast(EventDict, context))


def clear_context() -> None:
    """Clear request-scoped fields from the current execution context."""
    structlog.contextvars.clear_contextvars()


def _resolve_log_level(level: str | int) -> int:
    """Convert a standard logging level name or integer to its numeric value."""
    if isinstance(level, int):
        return level

    resolved_level = logging.getLevelName(level.upper())
    if not isinstance(resolved_level, int):
        raise ValueError(f"Unsupported log level: {level}")

    return resolved_level
