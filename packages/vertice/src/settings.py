from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    PGSQL_HOST: str
    PGSQL_USER: str
    PGSQL_PASSWORD: str
    PGSQL_DB: str
    PGSQL_PORT: int = 5432
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
