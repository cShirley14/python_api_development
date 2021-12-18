from pydantic import BaseSettings

class Settings (BaseSettings):
    db_url: str
    secret_key: str
    algorithm: str
    expiry_time: str

    class Config:
        env_file = ".env"