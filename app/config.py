import os
from functools import lru_cache
from pydantic import BaseSettings, Field

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

class Settings(BaseSettings):
    # astra_db_client_id: str
    db_client_id: str = Field(..., env="ASTRA_DB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_DB_CLIENT_SECRET")
    # aws_acces_key: str = Field(..., env="AWS_ACCESS_KEY")
    # aws_secret_key: str = Field(..., env="AWS_SECRET_KEY")

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()