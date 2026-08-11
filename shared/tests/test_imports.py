"""Import tests for the shared library package."""

from shared.sample import get_package_name


def test_shared_package_is_importable() -> None:
    """The workspace installs the shared package for other services to import."""
    assert get_package_name() == "physical-ai-partner-shared"
