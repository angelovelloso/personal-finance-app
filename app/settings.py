from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='/workspaces/financeiro-pessoal/app/.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
    DATABASE_URL_ALTERNATIVE: str
    DB_URL_COMPLETE: str
    API_BASE_URL: str
