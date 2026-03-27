from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"

    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str = "facturas"
    MAX_UPLOAD_SIZE_MB: int = 10

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"


settings = Settings()
