import pytest

from pylegifrance.config import ApiConfig
from pylegifrance.client import LegifranceClient


@pytest.fixture(scope="module")
def api_client() -> LegifranceClient:
    """Create a real Legifrance client for integration tests."""
    config = ApiConfig.from_env()
    return LegifranceClient(config=config)
