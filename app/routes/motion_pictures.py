from flask import Blueprint, request, jsonify
from app.models import MotionPictures, WatchList, Account
from app import db
from .utils import token_required
from datetime import datetime

motion_pictures = Blueprint("motion_pictures", __name__)


@motion_pictures.route("/api/add-to-watchlist", methods=["POST"])
@token_required
def add_to_watchlist(current_user):
    try:
        data = request.get_json()

        new_motion_picture = MotionPictures(
            title=data["title"],
            external_id=data["external_id"],
            poster_path=data["poster_path"],
            type=data["type"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.session.add(new_motion_picture)
        db.session.commit()

        new_watch_list = WatchList(
            account_id=current_user.account.id,
            motion_picture_id=new_motion_picture.id,
            watched=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.session.add(new_watch_list)
        db.session.commit()

        return jsonify(new_watch_list.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@motion_pictures.route("/api/update-watchlist/<int:watchlist_id>", methods=["PUT"])
@token_required
def update_watchlist(current_user, watchlist_id):
    try:
        data = request.get_json()
        watched = data["watched"]
        updated_at = datetime.now()

        watchlist_entry = WatchList.query.filter_by(
            id=watchlist_id, account_id=current_user.account.id
        ).first()
        if not watchlist_entry:
            return jsonify({"error": "Watchlist entry not found"}), 404

        if watched is not None:
            watchlist_entry.watched = watched
        watchlist_entry.updated_at = updated_at

        db.session.commit()

        return jsonify(watchlist_entry.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500