from flask import Flask

from routes.auth import auth_bp
from routes.user import user_bp
from routes.conversation import conversation_bp
from routes.message import message_bp

def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(conversation_bp, url_prefix="/api/conversations")
    app.register_blueprint(message_bp, url_prefix="/api/messages")