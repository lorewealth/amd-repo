from pathlib import Path

import pytest


@pytest.fixture
def logs_dir():
    return Path(__file__).parent.parent.parent / "logs"
