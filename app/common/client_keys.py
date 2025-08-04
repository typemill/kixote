import sqlite3
from flask import Blueprint, request, jsonify, current_app
from .config import Config

DB_PATH = Config.DB_PATH

def init_client_keys_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS client_keys (
        client_id TEXT PRIMARY KEY,
        api_key TEXT UNIQUE,
        license TEXT,
        created_at TEXT
    )''')
    conn.close()

def add_client_key(client_id, api_key, license):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO client_keys (client_id, api_key, license, created_at) VALUES (?, ?, ?, datetime('now'))",
        (client_id, api_key, license)
    )
    conn.commit()
    conn.close()

def get_client_key(api_key):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT client_id, license FROM client_keys WHERE api_key=?", (api_key,))
    row = cur.fetchone()
    conn.close()
    return row

def list_client_keys():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT client_id, license, created_at FROM client_keys")
    rows = cur.fetchall()
    conn.close()
    return [
        {"client_id": r[0], "license": r[1], "created_at": r[2]}
        for r in rows
    ]

def delete_client_key(client_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE client_keys SET api_key=NULL WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()

def update_client_key(client_id, new_api_key):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE client_keys SET api_key=?, created_at=datetime('now') WHERE client_id=?", (new_api_key, client_id))
    conn.commit()
    conn.close()

def remove_client(client_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM client_keys WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()

def get_client_by_id(client_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT client_id FROM client_keys WHERE client_id=?", (client_id,))
    row = cur.fetchone()
    conn.close()
    return row