import os

class Config:
    """Base configuration class."""
    LOGIN = os.environ.get("LOGIN", "True").lower() == "true"
    ADMIN_KEY = os.environ.get("ADMIN_KEY", "")
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
    CLIENT_LIMITS = {
        "maker": int(os.environ.get("CLIENT_LIMIT_MAKER", 220)),
        "business": int(os.environ.get("CLIENT_LIMIT_BUSINESS", 1220))
    }
    DB_PATH = os.environ.get("KIXOTE_DB_PATH", "/data/clients.db")
    
    # NOT IN USE    
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    TESTING = os.environ.get("TESTING", "True") == "True"
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///yourdatabase.db")

    # Example for email configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.yourdomain.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "your-email@example.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "your-email-password")