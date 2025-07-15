# %% load libraries
import sqlite3
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.common.config import Config
from app.common.rate_limiter import rate_limit
from datetime import datetime
from flask import current_app

DB_PATH = Config.DB_PATH


# %% create blueprint
check_bp = Blueprint("check", __name__)

# %% routes
@check_bp.route("/", methods=["GET"])
def check():
    return jsonify({"message": "Check service is running!"})

@check_bp.route("/auth", methods=["GET"])
@jwt_required()
def auth():
    return jsonify({"message": "Auth check is successful!"})

@check_bp.route("/limit", methods=["GET"])
@jwt_required()
@rate_limit(cost=1)
def limit():
    return jsonify({"message": "Rate limit is enough!"})

@check_bp.route("/rate", methods=["GET"])
@jwt_required()
def rate():
    claims = get_jwt()
    client_id = claims["sub"]
    license_type = claims.get("license")
    if not license_type:
        return jsonify({"error": "No license type found in token"}), 400

    limit = current_app.config["CLIENT_LIMITS"].get(license_type, 220)
    month = datetime.utcnow().strftime("%Y-%m")

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(usage) FROM rate_limit WHERE client_id=? AND date LIKE ?", (client_id, f"{month}-%"))
        row = cur.fetchone()
        usage = row[0] if row and row[0] is not None else 0

    return jsonify({
        "client_id": client_id,
        "license": license_type,
        "monthly_limit": limit,
        "used_this_month": usage,
        "remaining_this_month": max(0, limit - usage)
    })