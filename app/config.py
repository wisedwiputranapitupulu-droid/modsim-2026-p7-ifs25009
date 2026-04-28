import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = os.getenv("APP_PORT", 5000)
    BASE_URL = os.getenv("LLM_BASE_URL", "").rstrip("/")
    LLM_TOKEN = os.getenv("LLM_TOKEN", "").strip()
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not BASE_URL or not LLM_TOKEN:
        raise RuntimeError(
            "Environment variables LLM_BASE_URL and LLM_TOKEN must be set in .env"
        )
