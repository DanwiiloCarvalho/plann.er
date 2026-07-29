from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: str
    DATABASE_URL: str | None = None
    TEST_DATABASE_URL: str | None = None
    API_PREFIX: str | None = None
    OWNER_NAME: str
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')


settings = Settings()
