# Kixote Client API – Quick Reference


## Admin Routes

The following routes are always awailable with the admin key:

### Get Client

Get a client with a client id.

```sh
curl -X GET http://localhost:5000/auth/get_client \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: 123abc" \
  -d '{"client_id": "testclient"}'
```

**Response:**

```json
  {
    "client_id": "testclient",
    "created_at": "2025-06-19 05:53:13",
    "license": "maker"
  }
```

---

### List Clients

List all registered clients with truncated ids

```sh
curl -X GET http://localhost:5000/auth/list_clients \
  -H "X-ADMIN-KEY: 123abc"
```

**Response:**

```json
[
  {
    "client_id": "testclient",
    "created_at": "2025-06-19 05:53:13",
    "license": "maker"
  }
]
```

---


### Delete Client 

Delete a client with a client id.

```sh
curl -X DELETE http://localhost:5000/auth/delete_client \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: 123abc" \
  -d '{"client_id": "testclient"}'
```

**Response:**
```json
{
  "message": "Client deleted",
  "client_id": "testclient"
}
```

---

## Admin Routes (LOGIN_REQUIRED)

The following routes are only available if there is a value set for LOGIN_REQUIRED. With this routes the admin can create new clients manually and manage api keys for clients to authenticate and retrieve the JWT.

### Create Client

Create a new client and receive an API key.

```sh
curl -X POST http://localhost:5000/auth/create_client \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: admin123" \
  -d '{"client_id": "testclient", "license": "maker"}'
```

**Response:**
```json
{
  "api_key": "YOUR_CLIENT_API_KEY",
  "client_id": "testclient",
  "license": "maker"
}
```

---

### Recreate Client API Key

Generate a new API key for an existing client.

```sh
curl -X POST http://localhost:5000/auth/recreate_client_key \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: 123abc" \
  -d '{"client_id": "testclient"}'
```

**Response:**
```json
{
  "api_key": "YOUR_NEW_CLIENT_API_KEY",
  "client_id": "testclient",
  "message": "Client key recreated"
}
```

---

### Revoke Client API Key

Revoke (disable) a client's API key.

```sh
curl -X POST http://localhost:5000/auth/revoke_client_key \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: 123abc" \
  -d '{"client_id": "testclient"}'
```

**Response:**
```json
{
  "client_id": "testclient",
  "message": "Client key revoked"
}
```