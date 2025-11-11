"""
Configuration settings for the task planning service.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/task_planner"
    database_echo: bool = False

    # API settings
    api_title: str = "Task Planning Service"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Scheduler settings
    solver_time_limit: int = 60  # seconds
    default_solver: str = "ortools"  # or "cpoptimizer"

    # Logging
    log_level: str = "INFO"

    # Report settings
    report_template_dir: str = "templates/reports"
    report_output_dir: str = "output/reports"


settings = Settings()
