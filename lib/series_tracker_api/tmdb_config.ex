defmodule SeriesTrackerApi.TMDbConfig do
  def api_base_url, do: "https://api.themoviedb.org/3"
  def api_key, do: Application.get_env(:series_tracker_api, SeriesTrackerApi.TMDbConfig)[:api_key]
end
