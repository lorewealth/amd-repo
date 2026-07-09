from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class pydSettings(BaseSettings):
    database_url: str
    frontend_origin: str
    max_upload_bytes: int = 5 * 1024**2
    jwt_secret: str
    google_client_id: str
    google_client_secret: str
    allowed_email_list: str

    model_config = SettingsConfigDict(env_file=ENV_PATH)

    @property
    def max_upload_size_view(self):
        return f"{self.max_upload_bytes / (1024**2)}MB"


@lru_cache
def get_settings():
    return pydSettings()
