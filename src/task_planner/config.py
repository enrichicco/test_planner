"""Configuration management for task planner service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/task_planner"

    # Application settings
    app_name: str = "Task Planner Service"
    debug: bool = False

    # Planning settings
    max_planning_horizon_days: int = 90
    default_working_hours_per_day: int = 8


settings = Settings()
