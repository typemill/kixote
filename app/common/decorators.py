from flask import jsonify
from flask_jwt_extended import get_jwt
from app.common.init_db import get_db
from app.common.limiter_instance import limiter
from functools import wraps
from .config import Config
from datetime import datetime
from app import limiter


def auto_add_client_if_needed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Config.LOGIN_REQUIRED:
            claims = get_jwt()
            client_id = claims.get("sub")
            plan = claims.get("data", {}).get("plan", "MAKER")
            if not client_id:
                return jsonify({"error": "Invalid token: missing client_id"}), 400
            if plan not in ("MAKER", "BUSINESS"):
                plan = "MAKER"
            conn = get_db()
            try:
                cur = conn.cursor()
                cur.execute("SELECT client_id FROM client_keys WHERE client_id=?", (client_id,))
                row = cur.fetchone()
                if not row:
                    conn.execute(
                        "INSERT INTO client_keys (client_id, api_key, license, created_at) VALUES (?, ?, ?, datetime('now'))",
                        (client_id, None, plan)
                    )
                    conn.commit()
            finally:
                conn.close()
        return f(*args, **kwargs)
    return decorated_function

def request_limit(limit: str):
    def decorator(f):
        f_limited = limiter.limit(limit)(f)

        @wraps(f_limited)
        def wrapped(*args, **kwargs):
            try:
                return f_limited(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": "Request limit exceeded", "message": str(e)}), 429

        return wrapped

    return decorator


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
