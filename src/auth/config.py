import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv("../.env")


class Settings(BaseSettings):
    authjwt_secret_key = os.getenv("SECRET_KEY")


settings = Settings()
