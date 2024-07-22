"""
Module for application factory.

This module provides the application factory for creating the Flask app instance, initializing
the database, and registering blueprints.

Functions:
    create_app: Creates and configures the Flask application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()


def create_app():
    """
    Create and configure the Flask application.

    This function creates the Flask app instance, configures it with settings from the Config class,
    initializes the database and migration extensions, and registers the main blueprint.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    from .models import User, Account, MotionPictures, WatchList

    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
