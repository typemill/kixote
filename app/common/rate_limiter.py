import sqlite3
from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps
from .config import Config
from datetime import datetime

DB_PATH = Config.DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS rate_limit (
        client_id TEXT,
        date TEXT,
        usage INTEGER,
        PRIMARY KEY (client_id, date)
    )''')
    return conn

def rate_limit(cost):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            client_id = claims["sub"]
            license_type = claims["license"]
            limit = Config.CLIENT_LIMITS[license_type]
            today = datetime.utcnow().strftime("%Y-%m-%d")

            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT usage FROM rate_limit WHERE client_id=? AND date=?", (client_id, today))
            row = cur.fetchone()
            usage = row[0] if row else 0

            if usage + cost > limit:
                conn.close()
                return jsonify({"error": "Rate limit exceeded"}), 429

            if row:
                cur.execute("UPDATE rate_limit SET usage=usage+? WHERE client_id=? AND date=?", (cost, client_id, today))
            else:
                cur.execute("INSERT INTO rate_limit (client_id, date, usage) VALUES (?, ?, ?)", (client_id, today, cost))
            conn.commit()
            conn.close()
            return f(*args, **kwargs)
        return decorated_function
    return decorator