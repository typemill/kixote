# Kixote Client API – Quick Reference

## Create Client

Create a new client and receive an API key.

```sh
curl -X POST http://localhost:5000/auth/create_client \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-KEY: 123abc" \
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

## List Clients

List all registered clients.

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

## Revoke API Key

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

---

## Recreate Client Key

Generate a new API key for an existing client.

```sh
curl -X POST http://localhost:5000/auth/create_client_key \
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

## Delete Client 

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

## Login

Obtain a JWT access token using your API key.

```sh
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "CLIENT_API_KEY"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```