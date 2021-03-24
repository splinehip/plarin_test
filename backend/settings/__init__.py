from pydantic import BaseSettings
from dotenv import find_dotenv


class Settings(BaseSettings):
    DEBUG: bool = False
    MONGODB_URL: str

    class Config:
        env_file = find_dotenv('settings.env')
        env_file_encoding = 'utf-8'
        env_prefix = 'plarin_test_'


settings = Settings()
