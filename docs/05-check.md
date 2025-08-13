# Kixote Check API – Quick Reference

## Auth Check

Verify your JWT token is valid.

```sh
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/check/auth
```


**Response:**

```json
{
  "message": "Auth check is successful!"
}
```
## Rate Limit Check

Check if the rate limiting works (will add 1 point to usage).

```sh
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/check/limit
```

**Response:**

```json
{
  "message": "Rate limit is enough!"
}
```

## Usage Statistics

Get your current monthly usage and remaining quota.

```sh
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/check/rate
```

**Response:**

```json
{
  "client_id": "testclient",
  "license": "maker",
  "monthly_limit": 220,
  "remaining_this_month": 219,
  "used_this_month": 1
}
```