from flask import request, jsonify
from functools import wraps
import jwt
from app.models import User
from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["public_id"]).first()
        except Exception as e:
            return jsonify({"message": "Unauthorized"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
