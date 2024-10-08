"""
Module for authentication routes.

This module defines the routes for user authentication including signup and login.

Blueprints:
    auth: The blueprint for authentication routes.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Account
from app import db
import jwt
from datetime import datetime, timedelta
from config import Config

auth = Blueprint("auth", __name__)


@auth.route("/api/signup", methods=["POST"])
def signup():
    """
    Sign up a new user.

    This route allows a new user to sign up by providing a username, email, and password.
    It creates a new user and account in the database.

    Returns:
        tuple: A JSON response with the new account data and a status code.
    """
    try:
        data = request.get_json()
        if "username" not in data or "email" not in data or "password" not in data:
            return jsonify({"error": "Invalid data"}), 400

        password = data["password"]
        password_hash = generate_password_hash(password)

        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=password_hash,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()

        new_account = Account(
            email=data["email"],
            user_id=new_user.id,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        )

        db.session.add(new_account)
        db.session.commit()

        return jsonify(new_account.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth.route("/api/login", methods=["POST"])
def login():
    """
    Log in a user.

    This route allows a user to log in by providing an email and password.
    It generates a JWT token if the credentials are valid.

    Returns:
        tuple: A JSON response with the JWT token and account data, or an error message.
    """
    data = request.get_json()

    if "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid data"}), 400

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        token = jwt.encode(
            {"public_id": user.id, "exp": datetime.now() + timedelta(minutes=30)},
            Config.SECRET_KEY,
            algorithm="HS256",
        )
        account = user.account
        return jsonify(
            {
                "token": token,
                "account": account.to_dict(),
            }
        )
    else:
        return jsonify({"error": "Invalid credentials"}), 401
