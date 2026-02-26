import pytest

from src.schemas.config_schema import AppConfig
from src.config_loader import get_config


@pytest.fixture(scope="session")
def app_config() -> AppConfig:
    return get_config()


@pytest.fixture(scope="session")
def base_url(app_config: AppConfig) -> str:
    return app_config.server.url