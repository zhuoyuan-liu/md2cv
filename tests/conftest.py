"""Shared test fixtures for md2cv."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_minimal() -> str:
    return (FIXTURES_DIR / "sample_minimal.md").read_text()


@pytest.fixture
def sample_short() -> str:
    return (FIXTURES_DIR / "sample_short.md").read_text()


@pytest.fixture
def sample_long() -> str:
    return (FIXTURES_DIR / "sample_long.md").read_text()


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR
