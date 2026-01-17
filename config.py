"""Configuration management for lead generation system."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Apollo.io API Configuration
    apollo_api_key: str

    # Search Parameters
    default_person_titles: str = "CEO,CTO,VP Engineering"
    default_company_size: str = "1-10,11-50,51-200"
    default_industry: str = "Computer Software,Information Technology"

    # Output Settings
    output_format: str = "json"
    max_results: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_person_titles_list(self) -> list[str]:
        """Convert comma-separated titles to list."""
        return [title.strip() for title in self.default_person_titles.split(",")]

    def get_company_sizes_list(self) -> list[str]:
        """Convert comma-separated company sizes to list."""
        return [size.strip() for size in self.default_company_size.split(",")]

    def get_industries_list(self) -> list[str]:
        """Convert comma-separated industries to list."""
        return [industry.strip() for industry in self.default_industry.split(",")]


# Global settings instance
settings = Settings()
