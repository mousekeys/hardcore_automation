from schemas.config_schema import AppConfig

def test_url_exists(base_url: str):
    """Basic sanity check — URL must be a valid HTTP address."""
    assert base_url.startswith("http"), f"Expected HTTP URL, got: {base_url}"


def test_config_server_fields(app_config: AppConfig):
    """Validate all server config fields are populated."""
    assert app_config.server.url , "Server URL is required"
    assert app_config.server.files_url, "Files URL is required"
    assert app_config.server.terminal_selector, "Terminal selector is required"


def test_config_hardcore_plus_fields(app_config: AppConfig):
    """Validate all hardcore_plus config fields are populated."""
    assert app_config.hardcore_plus.world_folder, "World folder is required"
    assert app_config.hardcore_plus.death_keywords, "Death keywords are required"
    assert app_config.hardcore_plus.max_logs > 0 , "Max logs must be a positive integer"