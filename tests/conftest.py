"""Shared pytest fixtures for hacker_screen tests."""

from unittest.mock import MagicMock

import pytest
from rich.console import Console


@pytest.fixture
def mock_console() -> MagicMock:
    """Create a mock Rich console that captures output silently.

    Returns:
        A MagicMock wrapping a Console with recording enabled.
    """
    console = MagicMock(spec=Console)
    console.width = 80
    console.print = MagicMock()
    return console


@pytest.fixture
def real_console() -> Console:
    """Create a real Rich console that writes to a string buffer.

    Returns:
        A Console instance with file output for testing.
    """
    import io

    return Console(file=io.StringIO(), width=80)
