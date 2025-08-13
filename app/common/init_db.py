import sqlite3
import os
from .config import Config

def get_db():
    db_path = Config.DB_PATH
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        raise FileNotFoundError(f"Database directory does not exist: {db_dir}")
    try:
        conn = sqlite3.connect(db_path)
        # Create all necessary tables if they don't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS rate_limit (
            client_id TEXT,
            date TEXT,
            usage INTEGER,
            PRIMARY KEY (client_id, date)
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS client_keys (
            client_id TEXT PRIMARY KEY,
            api_key TEXT,
            license TEXT,
            created_at TEXT
        )''')
        # Add more table creation statements as needed
        return conn
    except Exception as e:
        print(f"Database connection/init error: {e}")