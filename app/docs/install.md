# Kixote Installation Guide (Docker)

This guide explains how to set up and run the Kixote application using Docker.

---

## 1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your server or local machine.

---

## 2. Build the Docker Image

Open a terminal in the project root directory (where the `Dockerfile` is located) and run:

```sh
docker build -t kixote-app .
```

---

## 3. Prepare a Persistent Data Directory

Create a directory on your host to store the SQLite database:

```sh
mkdir -p /path/on/host/data
```

---

## 4. Run the Container

Start the application with environment variables and persistent storage:

```sh
docker run -d \
  -p 5000:5000 \
  -v /path/on/host/data:/data \
  -e KIXOTE_DB_PATH=/data/clients.db \
  -e LOGIN=true \
  -e ADMIN_KEY=your_admin_key \
  -e SECRET_KEY=your_secret_key \
  -e JWT_SECRET_KEY=your_jwt_secret \
  -e CLIENT_LIMIT_MAKER=220 \
  -e CLIENT_LIMIT_BUSINESS=1220 \
  --name kixote-app \
  kixote-app
```

- Replace `/path/on/host/data` with the persistant data directory on your host with a sqlite db.
- KIXOTE_DB_PATH=/data/clients.db is the path to the sqlite db inside the container.
- LOGIN=true activates the admin endpoints and the login routes to get JWT tokens.
- Replace `your_admin_key` with secure values to access the endpoints for admins.
- Replace `your_jwt_secret` with secure values to generate and validate a JWT.
- CLIENT_LIMIT_MAKER is the rate limit for a maker client.
- CLIENT_LIMIT_BUSINESS is the rate limit for a business client.

---

## 5. Access the Application

Open your browser and go to:

```

```

or use your server's IP address if running remotely.

---

## 6. Stopping and Removing the Container

To stop:

```sh
docker stop kixote-app
```

To remove:

```sh
docker rm kixote-app
```

---

You're ready to use Kixote!