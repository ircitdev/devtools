"""Application configuration using Pydantic Settings."""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration with validation via Pydantic."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Instagram
    instagram_username: str
    instagram_password: str
    instagram_session_file: str = "session.json"

    # Telegram
    telegram_bot_token: str
    admin_telegram_ids: str = ""  # Comma-separated IDs

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"

    # Rate Limiting
    check_interval_seconds: int = 60
    message_delay_min_seconds: int = 30
    message_delay_max_seconds: int = 60
    max_messages_per_hour: int = 50

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/bot.log"

    # Google Sheets
    google_sheets_enabled: bool = True
    google_credentials_file: str = "credentials.json"
    google_spreadsheet_id: str = ""

    @property
    def admin_ids_list(self) -> List[int]:
        """Parse comma-separated admin IDs into list of integers."""
        if not self.admin_telegram_ids:
            return []
        return [int(id_.strip()) for id_ in self.admin_telegram_ids.split(",") if id_.strip()]

    @property
    def session_file_path(self) -> Path:
        """Get session file as Path."""
        return Path(self.instagram_session_file)

    @property
    def log_file_path(self) -> Path:
        """Get log file as Path."""
        return Path(self.log_file)


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
