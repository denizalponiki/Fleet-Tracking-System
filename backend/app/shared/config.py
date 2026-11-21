"""Application settings read from the environment (NFR-OPS-02).

Every value can be set in `.env`; nothing secret is hard-coded. `JWT_SECRET` has no default,
so the API refuses to start without it.
"""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FleetSync API"
    api_prefix: str = "/api/v1"

    database_url: str = Field(
        default="postgresql+psycopg://fleet:change-me-local@localhost:5432/fleet",
        description="SQLAlchemy URL; inside Docker Compose the host is `db`.",
    )

    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_expires_seconds: int = 3600  # ADR-005: 60-minute access token
    jwt_issuer: str = "fleetsync"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]  # values come from the environment
