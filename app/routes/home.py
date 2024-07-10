from flask import Blueprint
import os
import requests
from dotenv import load_dotenv

load_dotenv()

home = Blueprint("home", __name__)

movie_url = "https://api.themoviedb.org/3/movie/popular"
tv_url = "https://api.themoviedb.org/3/tv/popular"

# Ensure proper handling of f-string with getenv inside quotes
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('MOVIE_DB_ACCESS_TOKEN')}",
}


@home.route("/api/home/latest-movies", methods=["GET"])
def latest_movies():
    response = requests.get(movie_url, headers=headers)
    return response.json()


@home.route("/api/home/latest-series", methods=["GET"])
def latest_series():
    response = requests.get(tv_url, headers=headers)
    return response.json()
