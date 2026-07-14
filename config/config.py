from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):


    DB_USER:str
    DB_PASSWORD:str
    DB_HOST: str = "localhost"
    DB_PORT: int= 5432
    DB_NAME: str


    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30



    model_config = SettingsConfigDict(
        env_file=".env"
    )



settings = Settings()

password = quote_plus(settings.DB_PASSWORD)



DATABASE_URL = f"postgresql://{settings.DB_USER}:{password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"