from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # astra_db_client_id: str
    db_client_id: str = Field(..., env="ASTRA_DB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_DB_CLIENT_SECRET")

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()