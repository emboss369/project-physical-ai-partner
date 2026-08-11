"""Typed configuration primitives for independently configured services."""

from .settings import BaseServiceSettings, service_settings_config

__all__ = ["BaseServiceSettings", "service_settings_config"]
