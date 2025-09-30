import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__name__).resolve().parent / ".env")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

DB_NAME = os.getenv("DB_NAME")
print("Loaded DB_HOST:", DB_HOST)  # Add this line to debug


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
ADMIN_REMEMBER_ME_EXPIRE_MINUTES = 10080  # 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 43200  # 30 days

MEDIA_DIR = "media"
MEDIA_URL = "/media"
MEDIA_PATH = Path(MEDIA_DIR)
MEDIA_PATH.mkdir(exist_ok=True, parents=True)

STATIC_DIR = "static"
STATIC_URL = "/static"
STATIC_PATH = Path(STATIC_DIR)
STATIC_PATH.mkdir(exist_ok=True, parents=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB