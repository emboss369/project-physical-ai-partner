"""Common Pydantic Settings configuration for project services."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base class for validated, immutable service configuration.

    Services define their own fields and use :func:`service_settings_config` to
    select an environment-variable prefix. Values are resolved by
    pydantic-settings from initialization arguments, environment variables,
    optional local ``.env`` files, and defaults in that order.
    """

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
        frozen=True,
    )


def service_settings_config(*, env_prefix: str) -> SettingsConfigDict:
    """Return standard settings metadata for one independently deployed service.

    Args:
        env_prefix: Uppercase, underscore-terminated environment prefix, such
            as ``"LLM_"`` or ``"MEMORY_"``.

    Raises:
        ValueError: If ``env_prefix`` is empty or does not end with an underscore.
    """
    if not env_prefix or not env_prefix.endswith("_"):
        raise ValueError("env_prefix must be non-empty and end with an underscore")

    return SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix=env_prefix,
        extra="ignore",
        frozen=True,
    )
