# %% load libraries
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.common.decorators import auto_add_client_if_needed, rate_limit, request_limit
from app.common.jwt_blacklist import BLACKLIST
from app.common.config import Config
from app.common.client_keys import (
    insert_client, select_clients, select_client_by_id, select_client_by_key,
    delete_client_by_id, delete_client_key, update_client_key
)
import secrets

# %% create blueprint
auth_bp = Blueprint("auth", __name__)

# %% routes


@auth_bp.route("/list_clients", methods=["GET"])
@request_limit("1 per second")
def list_clients():
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    clients = select_clients()
    return jsonify(clients), 200

@auth_bp.route("/get_client", methods=["GET"])
@request_limit("1 per second")
def get_client():
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400
    client = select_client_by_id(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client), 200

@auth_bp.route("/delete_client", methods=["DELETE"])
@request_limit("1 per second")
def delete_client():
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400
    existing = select_client_by_id(client_id)
    if not existing:
        return jsonify({"error": "Client not found"}), 404
    delete_client_by_id(client_id)
    # Verify deletion
    if select_client_by_id(client_id):
        return jsonify({"error": "Failed to delete client"}), 500
    return jsonify({"message": "Client deleted", "client_id": client_id}), 200


@auth_bp.route("/create_client", methods=["POST"])
@request_limit("1 per second")
def create_client():
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403

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

    existing = select_client_by_id(client_id)
    if existing:
        return jsonify({"error": "Client ID already exists"}), 400

    api_key = secrets.token_urlsafe(32)
    insert_client(client_id, api_key, license)

    # Verify insert
    inserted = select_client_by_id(client_id)
    if not inserted:
        return jsonify({"error": "Failed to insert client"}), 500

    return jsonify({
        "client_id": client_id,
        "api_key": api_key,
        "license": license
    }), 201


@auth_bp.route("/recreate_client_key", methods=["POST"])
@request_limit("1 per second")
def recreate_client_key():
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Not available"}), 403

    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400

    existing_client = select_client_by_id(client_id)
    if not existing_client:
        return jsonify({"error": "Client not found"}), 404

    new_api_key = secrets.token_urlsafe(32)
    update_client_key(client_id, new_api_key)

    # Verify update
    updated_client = select_client_by_key(new_api_key)
    if not updated_client:
        return jsonify({"error": "Client with new api key not found"}), 404

    return jsonify({
        "message": "Client key recreated",
        "client_id": client_id,
        "api_key": new_api_key
    }), 200


@auth_bp.route("/revoke_client_key", methods=["POST"])
@request_limit("1 per second")
def revoke_client_key():
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403

    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    client_id = data.get("client_id")
    if not client_id or not isinstance(client_id, str):
        return jsonify({"error": "Missing or invalid 'client_id'"}), 400

    delete_client_key(client_id)

    # Verify that the key is now null
    client_data = select_client_by_id(client_id)
    if not client_data:
        return jsonify({"error": "Client not found"}), 404
    if client_data.get("api_key") is not None:
        return jsonify({"error": "Failed to revoke client key"}), 500

    return jsonify({
        "message": "Client key revoked",
        "client_id": client_id
    }), 200

    
"""
@auth_bp.route("/get_client_by_key", methods=["GET"])
def get_client_by_key():
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403
    admin_key = request.headers.get("X-ADMIN-KEY")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    api_key = request.args.get("api_key")
    if not api_key:
        return jsonify({"error": "API key required"}), 400
    client = select_client_by_key(api_key)
    if client:
        client_id, license_type = client
        return jsonify({"client_id": client_id, "license": license_type}), 200
    else:
        return jsonify({"error": "Invalid API key"}), 404
"""

@auth_bp.route("/login", methods=["POST"])
@request_limit("10 per minute")
def login():
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403

    api_key = request.json.get("api_key")
    if not api_key:
        return jsonify({"error": "API key required"}), 400

    client = select_client_by_key(api_key)
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
    if not Config.LOGIN_REQUIRED:
        return jsonify({"error": "Not available"}), 404    
    if not Config.ADMIN_KEY:
        return jsonify({"error": "Admin key required"}), 403
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
