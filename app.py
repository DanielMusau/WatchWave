"""
Module to run the Flask application.

This module initializes the Flask app and sets up database migrations.
It runs the app in debug mode if executed as the main module.
"""

from app import app, db
from flask_migrate import Migrate

app = app
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
