# %% load libraries
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.common.rate_limiter import rate_limit
from app.common.jwt_blacklist import BLACKLIST
from app.common.config import Config
from app.common.client_keys import add_client_key, get_client_key, get_client_by_id, list_client_keys, delete_client_key, update_client_key
import secrets

# %% create blueprint
auth_bp = Blueprint("auth", __name__)

# %% routes

@auth_bp.route("/login", methods=["POST"])
def login():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Login not available"}), 403

    api_key = request.json.get("api_key")
    if not api_key:
        return jsonify({"error": "API key required"}), 400

    client = get_client_key(api_key)
    if client:
        client_id, license_type = client
        access_token = create_access_token(
            identity=client_id,
            additional_claims={"license": license_type}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid API key"}), 401

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Logout not available"}), 403

    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route("/create_client", methods=["POST"])
def create_client():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key not configured"}), 403
    
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    client_id = data.get("client_id")
    license = data.get("license")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400
    if not license or not isinstance(license, str):
        return jsonify({"error": "Missing or invalid 'license'"}), 400

    existing = get_client_by_id(client_id)
    if existing:
        return jsonify({"error": "Client ID already exists"}), 400

    api_key = secrets.token_urlsafe(32)
    add_client_key(client_id, api_key, license)
    return jsonify({"client_id": client_id, "api_key": api_key, "license": license}), 201

@auth_bp.route("/list_clients", methods=["GET"])
def list_clients():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Not available"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    clients = list_client_keys()
    return jsonify(clients), 200

@auth_bp.route("/revoke_client_key", methods=["POST"])
def revoke_client_key():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Not available"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400
    delete_client_key(client_id)
    return jsonify({"message": "Client key revoked", "client_id": client_id}), 200

@auth_bp.route("/create_client_key", methods=["POST"])
def recreate_client_key():
    if not Config.LOGIN or not Config.ADMIN_KEY:
        return jsonify({"error": "Not available"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400
    new_api_key = secrets.token_urlsafe(32)
    update_client_key(client_id, new_api_key)
    return jsonify({"message": "Client key recreated", "client_id": client_id, "api_key": new_api_key}), 200