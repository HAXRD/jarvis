from flask import Flask
from flask_cors import CORS

from extensions import db, jwt, migrate
from routes import register_blueprints
from config import config_by_name
from middlewares.auth_middleware import jwt_required_middleware

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    # Register middleware
    app.before_request(jwt_required_middleware)

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)