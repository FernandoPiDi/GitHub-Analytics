"""
Configuration for the application.
"""

from functools import lru_cache

from pydantic import AnyUrl, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    azure_openai_api_key: SecretStr
    azure_openai_endpoint: str
    azure_openai_deployment: str
    azure_openai_api_version: str = "2024-02-15-preview"
    github_graphql_url: AnyUrl = AnyUrl("https://api.github.com/graphql")
    codegen_gh_auth: SecretStr

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get the application settings."""
    return Settings()
