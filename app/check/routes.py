# %% load libraries
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.common.decorators import auto_add_client_if_needed, rate_limit, request_limit
from app.common.init_db import get_db
from datetime import datetime
from flask import current_app


# %% create blueprint
check_bp = Blueprint("check", __name__)

# %% routes
@check_bp.route("/", methods=["GET"])
@request_limit("1 per second")
def check():
    return jsonify({"message": "Check service is running!"})

@check_bp.route("/auth", methods=["GET"])
@jwt_required()
@request_limit("1 per second")
def auth():
    return jsonify({"message": "Auth check is successful!"})

@check_bp.route("/limit", methods=["GET"])
@jwt_required()
@request_limit("1 per second")
@rate_limit(cost=1)
def limit():
    return jsonify({"message": "Added 1 point to the rate limit!"})

@check_bp.route("/rate", methods=["GET"])
@jwt_required()
@request_limit("10 per minute")
@auto_add_client_if_needed
def rate():
    claims = get_jwt()
    client_id = claims["sub"]
    license_type = claims.get("data", {}).get("plan", "MAKER")
    if not license_type:
        return jsonify({"error": "No license type found in token"}), 400

    limit = current_app.config["CLIENT_LIMITS"].get(license_type, 220)
    month = datetime.utcnow().strftime("%Y-%m")
    usage = get_monthly_usage(client_id, month)

    return jsonify({
        "license": license_type,
        "monthly_limit": limit,
        "used_this_month": usage,
        "remaining_this_month": max(0, limit - usage)
    })

def get_monthly_usage(client_id, month):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT SUM(usage) FROM rate_limit WHERE client_id=? AND date LIKE ?", (client_id, f"{month}-%"))
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else 0
    finally:
        conn.close()