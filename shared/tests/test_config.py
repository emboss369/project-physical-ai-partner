"""Tests for common service configuration primitives."""

import pytest
from pydantic import BaseModel, Field, ValidationError
from shared.config import BaseServiceSettings, service_settings_config


class ModelOptions(BaseModel):
    """Nested settings used to exercise the shared delimiter policy."""

    max_tokens: int = 512


class ExampleSettings(BaseServiceSettings):
    """Example service settings using the shared configuration policy."""

    model_config = service_settings_config(env_prefix="EXAMPLE_")

    api_url: str = Field(default="", min_length=1)
    model: ModelOptions = ModelOptions()


def test_settings_validate_environment_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment values are parsed and nested values use double underscores."""
    monkeypatch.setenv("EXAMPLE_API_URL", "http://localhost:8000")
    monkeypatch.setenv("EXAMPLE_MODEL__MAX_TOKENS", "1024")

    settings = ExampleSettings()

    assert settings.api_url == "http://localhost:8000"
    assert settings.model.max_tokens == 1024


def test_settings_fail_when_required_value_is_missing() -> None:
    """Missing required values fail during settings construction."""
    with pytest.raises(ValidationError):
        ExampleSettings()


def test_service_prefix_must_end_with_an_underscore() -> None:
    """Service prefixes remain unambiguous in the process environment."""
    with pytest.raises(ValueError, match="end with an underscore"):
        service_settings_config(env_prefix="EXAMPLE")
