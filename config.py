from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv(override=True) 
print("ENV DATABASE_URL =", os.getenv("DATABASE_URL"))
print("CWD =", os.getcwd())


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"

    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_CSRF_PROTECT = False
