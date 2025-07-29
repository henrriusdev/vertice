from pydantic_settings import BaseSettings
import pytz

class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    PGSQL_HOST: str
    PGSQL_USER: str
    PGSQL_PASSWORD: str
    PGSQL_DB: str
    PGSQL_PORT: int = 5432
    DEBUG: bool = True
    TIMEZONE: str = "America/Caracas"  # GMT-4 Venezuela timezone

    class Config:
        env_file = ".env"

    @property
    def timezone_obj(self):
        """Get the timezone object for the configured timezone"""
        return pytz.timezone(self.TIMEZONE)

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