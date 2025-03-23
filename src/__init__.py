from flask import Flask
from flask_cors import CORS
from config import limiter
from flask_jwt_extended import JWTManager
from datetime import timedelta
import secrets
import os

from .routes import ListScrapingResultRoute, AuthenticateRoute, VerifyTokenRoute

def init_app(config):

    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
    limiter.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(ListScrapingResultRoute.main)
    app.register_blueprint(AuthenticateRoute.main)
    app.register_blueprint(VerifyTokenRoute.main)

    return app