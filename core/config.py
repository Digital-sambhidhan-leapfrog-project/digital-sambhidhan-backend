import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    
    # Database
    DB_USER: str = os.getenv('MYSQL_USER')
    DB_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
    DB_NAME: str = os.getenv('MYSQL_DB')
    DB_HOST: str = os.getenv('MYSQL_SERVER')
    DB_PORT: str = os.getenv('MYSQL_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:%s@{DB_HOST}:{DB_PORT}/{DB_NAME}" % quote_plus(DB_PASSWORD)
    
    # JWT 
    JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)

    # Email
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_FROM')
    MAIL_PORT: int = os.getenv('MAIL_PORT')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME: str = os.getenv('MAIL_FROM_NAME')

mail_conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM = os.getenv('MAIL_FROM'),
    MAIL_PORT = os.getenv('MAIL_PORT'),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

    
def get_settings() -> Settings:
    return Settings()