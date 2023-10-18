defmodule SeriesTrackerApiWeb.Router do
  use SeriesTrackerApiWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/api", SeriesTrackerApiWeb do
    pipe_through :api

    resources "/users", UserController
    resources "/watched_items", WatchedItemController, except: [:new, :edit]

    get "/search_series", SeriesController, :search_series
    get "/search_movie", SeriesController, :search_movie
    get "/daily_trending_movies", SeriesController, :get_daily_trending_movies
    get "/weekly_trending_movies", SeriesController, :get_weekly_trending_movies
    get "/daily_trending_tv", SeriesController, :get_daily_trending_tv
    get "/weekly_trending_tv", SeriesController, :get_weekly_trending_tv
    get "/trending_tv", SeriesController, :get_trending_tv
    get "/upcoming_movies", SeriesController, :get_upcoming_movies

    post "/login", SessionController, :login
    post "/logout", SessionController, :logout
  end

  # Enable LiveDashboard and Swoosh mailbox preview in development
  if Application.compile_env(:series_tracker_api, :dev_routes) do
    # If you want to use the LiveDashboard in production, you should put
    # it behind authentication and allow only admins to access it.
    # If your application does not have an admins-only section yet,
    # you can use Plug.BasicAuth to set up some basic authentication
    # as long as you are also using SSL (which you should anyway).
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through [:fetch_session, :protect_from_forgery]

      live_dashboard "/dashboard", metrics: SeriesTrackerApiWeb.Telemetry
      forward "/mailbox", Plug.Swoosh.MailboxPreview
    end
  end
end
