from pydantic import BaseModel, Field
from typing import List


class ServerConfig(BaseModel):
    url: str
    files_url: str
    terminal_selector: str


class HardcorePlusConfig(BaseModel):
    world_folder: str
    death_keywords: List[str]
    max_logs: int = Field(default=100)
    
class AuthConfig(BaseModel):
    login_url: str
    panel_url: str


class AppConfig(BaseModel):
    server: ServerConfig
    hardcore_plus: HardcorePlusConfig
    auth: AuthConfig