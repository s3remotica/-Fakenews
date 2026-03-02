from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Real-Time Fake News Detection API'
    cors_origins: str = 'http://localhost:3000'
    model_name: str = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
    request_timeout_seconds: int = 6
    max_text_length: int = 5000
    rate_limit_per_minute: int = 30
    enable_url_analysis: bool = True
    enable_history: bool = True
    database_url: str = 'sqlite:///./app.db'
    placeholder_model_notice: str = (
        'Using a sentiment model as placeholder baseline. Replace with a misinformation fine-tuned model for production use.'
    )


settings = Settings()
