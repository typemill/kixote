# Kixote Client API – Quick Reference

The following routes are only available if a value for LOGIN_REQUIRED is set

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

# Logout

Add the current JWT to the blacklist.

```sh
curl -X POST http://localhost:5000/auth/logout \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```
