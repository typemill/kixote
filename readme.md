# Kixote

**Kixote** is a docker app and backend service for [Typemill](https://typemill.net), providing various API services including authentication, PDF generation via WeasyPrint, and AI services in future. It is designed to support Typemill instances, but can also be self-hosted in future to host these services on your own.

## Requirements

- Python 3.12+
- Flask
- Flask-JWT-Extended
- Flask-Limiter
- SQLite (optional for persistent rate limiting)
- Other dependencies listed in `requirements.txt`
- Docker

## Documentation

Full documentation and API usage can be found in the docs-folder.

## Notes

This project is **not ready** for self-hosting yet.