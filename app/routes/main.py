# This module defines the routes for the application
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Account
from sqlalchemy.sql import func
from app import db
import jwt
from datetime import datetime, timedelta
from functools import wraps
from config import Config

main = Blueprint("main", __name__)


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Unauthorized"}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@main.route("/api/signup", methods=["POST"])
def signup():
    """This function creates a new user account and associated account."""
    try:
        data = request.get_json()
        if "username" not in data or "email" not in data or "password" not in data:
            return jsonify({"error": "Invalid data"}), 400

        username = data["username"]
        email = data["email"]
        password = data["password"]
        created_at = func.now()
        updated_at = func.now()

        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=created_at,
            updated_at=updated_at,
        )

        db.session.add(new_user)

        db.session.commit()

        new_account = Account(
            email=email,
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


@main.route("/api/login", methods=["POST"])
def login():
    """Authenticating a user login"""
    data = request.get_json()

    if "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid data"}), 400

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        # generate a new JWT token with the user id
        token = jwt.encode(
            {"public_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
            Config.SECRET_KEY,
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
