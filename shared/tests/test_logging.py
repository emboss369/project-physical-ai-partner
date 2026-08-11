"""Tests for the shared structured logging API."""

import json

from pytest import CaptureFixture
from shared.logging import bind_context, clear_context, configure_logging, get_logger


def test_get_logger_emits_info_to_console(capsys: CaptureFixture[str]) -> None:
    """Console logging emits an INFO event and its structured fields."""
    configure_logging(json_logs=False)

    get_logger("shared.tests").info("application_started", service="test-service")

    output = capsys.readouterr().out
    assert "application_started" in output
    assert "service=test-service" in output


def test_debug_logs_respect_the_configured_level(capsys: CaptureFixture[str]) -> None:
    """DEBUG events are emitted only after the level is lowered to DEBUG."""
    configure_logging(level="INFO", json_logs=True)
    get_logger("shared.tests").debug("debug_hidden")
    assert capsys.readouterr().out == ""

    configure_logging(level="DEBUG", json_logs=True)
    get_logger("shared.tests").debug("debug_visible")

    event = json.loads(capsys.readouterr().out)
    assert event["event"] == "debug_visible"
    assert event["level"] == "debug"


def test_json_logs_include_bound_context(capsys: CaptureFixture[str]) -> None:
    """Request-scoped context is included in JSON log events."""
    clear_context()
    configure_logging(json_logs=True)
    bind_context(correlation_id="request-123")

    try:
        get_logger("shared.tests").info("request_completed")
        event = json.loads(capsys.readouterr().out)
    finally:
        clear_context()

    assert event["correlation_id"] == "request-123"
    assert event["event"] == "request_completed"
