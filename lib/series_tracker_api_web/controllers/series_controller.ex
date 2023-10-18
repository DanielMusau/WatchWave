defmodule SeriesTrackerApiWeb.SeriesController do
  use SeriesTrackerApiWeb, :controller
  alias SeriesTrackerApi.TMDbClient

  # search for series
  def search_series(conn, query_params) do
    case TMDbClient.get("/search/tv", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # search for movies
  def search_movie(conn, query_params) do
    case TMDbClient.get("/search/movie", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # Get daily trending movies
  def get_daily_trending_movies(conn, query_params) do
    case TMDbClient.get("/trending/movie/day", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # Get weekly trending movies
  def get_weekly_trending_movies(conn, query_params) do
    case TMDbClient.get("/trending/movie/week", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # Get daily trending tv shows
  def get_daily_trending_tv(conn, query_params) do
    case TMDbClient.get("/trending/tv/day", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # Get weekly trending tv shows
  def get_weekly_trending_tv(conn, query_params) do
    case TMDbClient.get("/trending/tv/week", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end

  # Get Upcoming Movies
  def get_upcoming_movies(conn, query_params) do
    case TMDbClient.get("/movie/upcoming", query_params) do
      {:ok, results} ->
        json(conn, results)

      {:error, reason} ->
        json(conn, %{"error" => reason})
    end
  end
end
