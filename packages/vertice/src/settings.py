from pydantic_settings import BaseSettings

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

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.PGSQL_USER}:{settings.PGSQL_PASSWORD}@{settings.PGSQL_HOST}:{settings.PGSQL_PORT}/{settings.PGSQL_DB}",
    },
    "apps": {
        "models": {
            "models": [
                "src.model",        
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}