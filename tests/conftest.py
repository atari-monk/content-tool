# tests/conftest.py
"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest
from typing import Any, Dict


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_config() -> Dict[str, Dict[str, Any]]:
    """Provide sample configuration."""
    return {
        "defaults": {
            "ignore_dirs": [".git", "__pycache__"],
            "output_format": "markdown",
        }
    }
