import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")


SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

# Path or URI to the SQLite database file
DATABASE_URI = os.getenv("DATABASE_URI", str(BASE_DIR / "orders.db"))

# Placeholder for external service access
API_KEY = os.getenv("API_KEY")

