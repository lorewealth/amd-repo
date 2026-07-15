from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class pydSettings(BaseSettings):
    database_url: str
    frontend_origin: str
    max_upload_bytes: int = 5 * 1024**2
    jwt_secret: str
    google_client_id: str
    google_client_secret: str
    allowed_email_list: set[str]

    model_config = SettingsConfigDict(env_file=ENV_PATH)

    @property
    def max_upload_size_view(self):
        return f"{self.max_upload_bytes / (1024**2)}MB"

    @field_validator("allowed_email_list", mode="before")
    @classmethod
    def normalize_emails(cls, value: set[str]) -> set[str]:
        if isinstance(value, list):
            return {email.lower().strip() for email in value}
        return value



@lru_cache
def get_settings():
    return pydSettings()
