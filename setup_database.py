import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import date

# Load environment variables from .env file
load_dotenv()

# --- DATABASE CONNECTION SETUP ---
DB_HOST = "127.0.0.1" # Connecting via Cloud SQL Proxy
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "leave_app_db" # Ensure this matches the DB name in Cloud SQL

if not DB_PASSWORD:
    raise ValueError("❌ DB_PASSWORD environment variable not found.")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
