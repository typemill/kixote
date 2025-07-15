# %% import libraries
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from .common.config import Config
from .common.rate_limiter import get_db
from .common.client_keys import init_client_keys_db
from .common.jwt_blacklist import is_token_revoked
from .auth.routes import auth_bp
from .check.routes import check_bp
from app.weasyprint.routes import weasyprint_bp
# from app.ki_services import ki_services_bp
# from app.agent_services import agent_services_bp

# %% create app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    # Initialize database
    get_db()

    # Initialize client keys database if admin key is set
    if Config.ADMIN_KEY:
        init_client_keys_db()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(check_bp, url_prefix="/check")
    app.register_blueprint(weasyprint_bp, url_prefix="/weasyprint")
    # app.register_blueprint(ki_services_bp, url_prefix="/ki")
    # app.register_blueprint(agent_services_bp, url_prefix="/agents")
    
    @app.route("/")
    def home():
        return render_template("index.html")
    
    return app

# %%
