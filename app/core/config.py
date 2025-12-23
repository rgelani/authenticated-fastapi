from pydentic import BaseSettings

class Settings(BaseSettings):
    #App Name
    APP_NAME: str = "Authenticated FastAPI"

    #Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    #Database
    DATABASE_DB_PATH: str = "auth.db"

    class Config:
        env_file = ".env"

settings = Settings()        