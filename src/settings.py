import os
import sys

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    if sys.platform.lower() == "win32" or os.name.lower() in ["nt", "darwin", "posix"]:
        from dotenv import load_dotenv

        load_dotenv()
    db_engine: str = Field(os.environ.get("DB_ENGINE"))
    db_user: str = Field(os.environ.get("DB_USER"))
    db_password: str = Field(os.environ.get("DB_PASSWORD"))
    db_host: str = Field(os.environ.get("DB_HOST"))
    db_port: int = Field(os.environ.get("DB_PORT"))
    db_name: str = Field(os.environ.get("DB_NAME"))

    project_name: str = Field(os.environ.get("PROJECT_NAME"))
    project_description: str = Field(os.environ.get("PROJECT_DESCRIPTION"))
    project_version: str = Field(os.environ.get("PROJECT_VERSION"))
    is_debug_mode: bool = Field(os.environ.get("DEBUG_MODE"))

    secret_key: str = Field(os.environ.get("SECRET_KEY"))
    algorithm: str = Field(os.environ.get("ALGORITHM"))
    access_token_expire_minutes: int = Field(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    )
    refresh_token_expire_days: int = Field(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))

    server_url: str = Field(os.environ.get("SERVER_URL"))
    kafka_bootstrap_servers: str = Field(
        os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    )

    smtp_server: str = Field(os.environ.get("SMTP_SERVER"))
    smtp_port: str = Field(os.environ.get("SMTP_PORT"))
    smtp_username: str = Field(os.environ.get("SMTP_USERNAME"))
    smtp_password: str = Field(os.environ.get("SMTP_PASSWORD"))
    mail_from: str = Field(os.environ.get("MAIL_FROM"))

    @property
    def database_url(self) -> str:
        return f"{self.db_engine}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        


settings: Settings | None = None


def get_settings() -> Settings:
    """
    Возвращает глобальные настройки проекта
    """
    global settings

    if not settings:
        settings = Settings()
    return settings
