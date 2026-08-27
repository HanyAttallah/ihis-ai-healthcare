import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """Base configuration for the iHIS application."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-change-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///ihis.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
