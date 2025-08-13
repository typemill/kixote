from flask import Blueprint, request, jsonify, current_app
from app.common.init_db import get_db

def insert_client(client_id, api_key, license):
    conn = get_db()
    conn.execute(
        "INSERT INTO client_keys (client_id, api_key, license, created_at) VALUES (?, ?, ?, datetime('now'))",
        (client_id, api_key, license)
    )
    conn.commit()
    conn.close()

def select_clients():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT client_id, license, created_at FROM client_keys")
    rows = cur.fetchall()
    conn.close()

    def truncate_id(cid):
        return cid if len(cid) <= 8 else cid[:8] + "..."

    return [
        {
            "client_id": truncate_id(r[0]),
            "license": r[1],
            "created_at": r[2]
        }
        for r in rows
    ]

def select_client_by_id(client_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT client_id, license FROM client_keys WHERE client_id=?", (client_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"client_id": row[0], "license": row[1]}
    return None

def select_client_by_key(api_key):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT client_id, license FROM client_keys WHERE api_key=?", (api_key,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_client_by_id(client_id):
    conn = get_db()
    conn.execute("DELETE FROM client_keys WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()

def delete_client_key(client_id):
    conn = get_db()
    conn.execute("UPDATE client_keys SET api_key=NULL WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()

def update_client_key(client_id, new_api_key):
    conn = get_db()
    conn.execute("UPDATE client_keys SET api_key=?, created_at=datetime('now') WHERE client_id=?", (new_api_key, client_id))
    conn.commit()
    conn.close()