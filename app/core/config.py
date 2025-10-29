from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI & ML Research Blog"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "a-very-secret-key-that-should-be-in-an-env-file"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True


settings = Settings()