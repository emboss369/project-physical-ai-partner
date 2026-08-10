"""Tests for the repository-wide Python workspace."""

import sys


def test_python_version_is_3_12() -> None:
    """The workspace must run on the project's supported Python version."""
    assert sys.version_info[:2] == (3, 12)
