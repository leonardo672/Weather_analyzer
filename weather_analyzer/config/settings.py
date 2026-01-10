from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Centralized, typed, validated configuration for the weather_analyzer system.
    All values come from environment variables or .env and are loaded once at startup.
    """

    # ----------------------
    # Application
    # ----------------------
    APP_NAME: str = "weather_analyzer"
    ENV: str = Field("local", description="local | staging | production")
    LOG_LEVEL: str = Field("INFO", description="DEBUG | INFO | WARNING | ERROR")

    # ----------------------
    # Weather API
    # ----------------------
    WEATHER_API_KEY: str
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    UNITS: str = "metric"

    # ----------------------
    # Cities
    # ----------------------
    # Default cities if nothing is provided in .env or CLI
    CITIES: List[str] = ["Stockholm", "London", "New York"]

    # ----------------------
    # PostgreSQL
    # ----------------------
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # ----------------------
    # Pipeline Behavior
    # ----------------------
    REQUEST_TIMEOUT: int = 10
    API_RETRIES: int = 3
    DB_RETRIES: int = 3
    SCHEDULER_INTERVAL_MINUTES: int = 10

    # ----------------------
    # Validators
    # ----------------------
    @validator("CITIES", pre=True)
    def split_cities(cls, value):
        """
        Allows CITIES to be defined as:
        CITIES=Berlin,Paris,Tokyo
        in .env or environment variables.
        """
        if isinstance(value, str):
            return [city.strip() for city in value.split(",") if city.strip()]
        return value

    # ----------------------
    # Pydantic config
    # ----------------------
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Cached singleton: loaded once per process
@lru_cache
def get_settings() -> Settings:
    return Settings()


# This is what the rest of the app imports
settings = get_settings()
