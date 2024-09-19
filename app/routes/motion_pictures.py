"""
Module for motion pictures routes.

This module defines the routes for adding to and updating the watchlist of motion pictures.

Blueprints:
    motion_pictures: The blueprint for motion pictures routes.
"""

from flask import Blueprint, request, jsonify
from app.models import MotionPictures, WatchList, Account
from app import db
from .utils import token_required
from datetime import datetime

motion_pictures = Blueprint("motion_pictures", __name__)


@motion_pictures.route("/api/add-to-watchlist", methods=["POST"])
@token_required
def add_to_watchlist(current_user):
    """
    Add a new motion picture to the watchlist.

    This route allows a user to add a new motion picture to their watchlist.

    Args:
        current_user (Account): The current authenticated user.

    Returns:
        tuple: A JSON response with the new watchlist entry data and a status code.
    """
    try:
        data = request.get_json()

        new_motion_picture = MotionPictures(
            title=data["title"],
            external_id=data["external_id"],
            poster_path=data["poster_path"],
            type=data["type"],
            overview=data["overview"],
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
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@motion_pictures.route("/api/update-watchlist/<int:watchlist_id>", methods=["PUT"])
@token_required
def update_watchlist(current_user, watchlist_id):
    """
    Update the watchlist entry.

    This route allows a user to update the watched status of a watchlist entry.

    Args:
        current_user (Account): The current authenticated user.
        watchlist_id (int): The ID of the watchlist entry to update.

    Returns:
        tuple: A JSON response with the updated watchlist entry data and a status code.
    """
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


@motion_pictures.route("/api/watchlist", methods=["GET"])
@token_required
def get_watchlist(current_user):
    """
    Get the motion pictures in the watchlist for the current user.

    This route allows a user to retrieve all motion pictures in their watchlist.

    Args:
        current_user (Account): The current authenticated user.

    Returns:
        tuple: A JSON response with the motion pictures data and a status code.
    """
    try:
        # Query the WatchList table to get motion picture IDs for the current user
        watchlist_entries = WatchList.query.filter_by(
            account_id=current_user.account.id
        ).all()

        # Extract motion picture IDs from watchlist entries
        motion_picture_ids = [entry.motion_picture_id for entry in watchlist_entries]

        # Query the MotionPictures table to get details for the motion picture IDs
        motion_pictures = MotionPictures.query.filter(
            MotionPictures.id.in_(motion_picture_ids)
        ).all()

        # Convert motion pictures to a list of dictionaries
        motion_picture_data = [
            motion_picture.to_dict() for motion_picture in motion_pictures
        ]

        return jsonify(motion_picture_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motion_pictures.route(
    "/api/remove-from-watchlist/<int:motion_picture_id>", methods=["DELETE"]
)
@token_required
def remove_from_watchlist(current_user, motion_picture_id):
    """
    Remove a motion picture from the watchlist.

    This route allows a user to remove a motion picture from their watchlist.

    Args:
        current_user (Account): The current authenticated user.
        motion_picture_id (int): The ID of the motion picture to remove from the watchlist.

    Returns:
        tuple: A JSON response confirming the removal and a status code.
    """
    try:
        # Find the watchlist entry for the current user and the specified motion picture
        watchlist_entry = WatchList.query.filter_by(
            account_id=current_user.account.id, motion_picture_id=motion_picture_id
        ).first()

        if not watchlist_entry:
            return jsonify({"error": "Watchlist entry not found"}), 404

        # Remove the entry from the watchlist
        db.session.delete(watchlist_entry)
        db.session.commit()

        return jsonify({"message": "Motion picture removed from watchlist"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
