"""
Module for home routes.

This module defines the routes for fetching the latest movies and series from an external API.

Blueprints:
    home: The blueprint for home routes.
"""

from flask import Blueprint, request
import os
import requests
from dotenv import load_dotenv
from .utils import token_required

load_dotenv()

home = Blueprint("home", __name__)

movie_url = "https://api.themoviedb.org/3/movie/popular"
tv_url = "https://api.themoviedb.org/3/tv/popular"
search_url = "https://api.themoviedb.org/3/search/multi"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('MOVIE_DB_ACCESS_TOKEN')}",
}


@home.route("/api/home/latest-movies", methods=["GET"])
@token_required
def latest_movies(current_user):
    """
    Fetch the latest popular movies.

    This route fetches the latest popular movies from the external API.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        dict: A JSON response containing the latest popular movies.
    """
    response = requests.get(movie_url, headers=headers)
    return response.json()


@home.route("/api/home/latest-series", methods=["GET"])
@token_required
def latest_series(current_user):
    """
    Fetch the latest popular TV series.

    This route fetches the latest popular TV series from the external API.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        dict: A JSON response containing the latest popular TV series.
    """
    response = requests.get(tv_url, headers=headers)
    return response.json()


@home.route("/api/home/search", methods=["GET"])
@token_required
def search(current_user):
    """
    Search for movies and series.

    This route searches for movies and series based on the query parameter.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        dict: A JSON response containing the search results.
    """
    query = request.args.get("query")
    response = requests.get(f"{search_url}?query={query}", headers=headers)
    return response.json()
