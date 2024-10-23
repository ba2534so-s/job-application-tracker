from flask import Blueprint

from .auth import bp as auth_bp
from .jobhuntr import bp as jobhuntr_bp

def init_app(app):
    app.register_blueprint(auth_bp)