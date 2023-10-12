defmodule SeriesTrackerApi.Repo do
  use Ecto.Repo,
    otp_app: :series_tracker_api,
    adapter: Ecto.Adapters.Postgres
end
