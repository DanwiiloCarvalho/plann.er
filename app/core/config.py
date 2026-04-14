from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    API_PREFIX: str | None = None
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')


settings = Settings()
