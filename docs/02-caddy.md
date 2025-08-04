# Reverse Proxy with Caddy

Caddy is a modern web server that makes it easy to serve your application securely over HTTPS. It is especially useful for Dockerized apps because it can automatically obtain and renew TLS certificates from Let’s Encrypt, and requires minimal configuration.  

---

## Why use Caddy?

- **Automatic HTTPS:** Instantly get and renew certificates from Let’s Encrypt.
- **Simple configuration:** Minimal setup compared to nginx or Apache.
- **Great for Docker:** Easily reverse-proxy to your app running in a container.

---


## Requirements

- Your domain (e.g., `yourdomain.com`) must point to your server’s public IP (DNS A record).
- Ports 80 and 443 must be open on your server.
- Your Flask/Docker app must be running and accessible at the server

## Install Caddy

### 1. Download and install caddy

```sh
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

### 2. Create a Caddyfile

```sh
sudo nano /etc/caddy/Caddyfile
```

Replace `yourdomain.com` with your actual domain name.

```
yourdomain.com {
    reverse_proxy localhost:5000
}
```

**Tip:**  
If your Docker container is on a user-defined Docker network, you can use the container name instead of `localhost` in the `reverse_proxy` directive (e.g., `reverse_proxy kixote-app:5000`).


### 3. Restart the service

```sh
sudo systemctl restart caddy
```

## Restricting Direct Access to Your App

To ensure your Flask/Docker app is only accessible through Caddy and not directly via your server’s IP and port, follow these recommendations:

### 1. If running directly on the host

Configure your Flask app to listen only on `127.0.0.1` (localhost) instead of `0.0.0.0`. Example in `run.py`:

  ```python
  if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5000)
  ```

### 2. If running in Docker

Do not publish port 5000 to all interfaces. Either:

- Omit the `-p` flag entirely and let Caddy connect via Docker network, or
- Use `-p 127.0.0.1:5000:5000` to bind only to localhost.

### 3. Firewall option

Block external access to port 5000 using your firewall (e.g., UFW or iptables), allowing only local connections.