from flask import Blueprint
import os
import requests
from dotenv import load_dotenv
from .utils import token_required

load_dotenv()

home = Blueprint("home", __name__)

movie_url = "https://api.themoviedb.org/3/movie/popular"
tv_url = "https://api.themoviedb.org/3/tv/popular"


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('MOVIE_DB_ACCESS_TOKEN')}",
}


@home.route("/api/home/latest-movies", methods=["GET"])
@token_required
def latest_movies(current_user):
    response = requests.get(movie_url, headers=headers)
    return response.json()


@home.route("/api/home/latest-series", methods=["GET"])
@token_required
def latest_series(current_user):
    response = requests.get(tv_url, headers=headers)
    return response.json()
