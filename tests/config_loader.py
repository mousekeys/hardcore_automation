
import yaml
import pytest
from pydantic import ValidationError
from typing import Optional

from schemas.config_schema import AppConfig


CONFIG_YAML_PATH = "../src/config.yaml"


def load_config_from_module() -> Optional[AppConfig]:
    """Try loading config from config.py module in the tests/ directory."""
    try:
        import config as cfg_module
        return AppConfig.model_validate(cfg_module.CONFIG)
    except ImportError:
        return None


def load_config_from_yaml(path: str = CONFIG_YAML_PATH) -> AppConfig:
    """Load and validate config from a YAML file."""
    try:
        with open(path, "r") as f:
            raw = yaml.safe_load(f) or {}
    except FileNotFoundError:
        pytest.fail(f"Config file not found: {path}")

    try:
        return AppConfig.model_validate(raw)
    except ValidationError as e:
        pytest.fail(f"Config validation failed:\n{e}")


def get_config() -> AppConfig:
    """Return config from module if available, otherwise fall back to YAML."""
    return load_config_from_module() or load_config_from_yaml()