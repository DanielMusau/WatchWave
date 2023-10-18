defmodule SeriesTrackerApiWeb.WatchedItemController do
  use SeriesTrackerApiWeb, :controller

  alias SeriesTrackerApi.WatchedItems
  alias SeriesTrackerApi.WatchedItems.WatchedItem

  action_fallback SeriesTrackerApiWeb.FallbackController

  def index(conn, _params) do
    watched_items = WatchedItems.list_watched_items()
    render(conn, :index, watched_items: watched_items)
  end

  def create(conn, %{"watched_item" => watched_item_params}) do
    with {:ok, %WatchedItem{} = watched_item} <-
           WatchedItems.create_watched_item(watched_item_params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", ~p"/api/watched_items/#{watched_item}")
      |> render(:show, watched_item: watched_item)
    end
  end

  def show(conn, %{"id" => id}) do
    watched_item = WatchedItems.get_watched_item!(id)
    render(conn, :show, watched_item: watched_item)
  end

  def update(conn, %{"id" => id, "watched_item" => watched_item_params}) do
    watched_item = WatchedItems.get_watched_item!(id)

    with {:ok, %WatchedItem{} = watched_item} <-
           WatchedItems.update_watched_item(watched_item, watched_item_params) do
      render(conn, :show, watched_item: watched_item)
    end
  end

  def delete(conn, %{"id" => id}) do
    watched_item = WatchedItems.get_watched_item!(id)

    with {:ok, %WatchedItem{}} <- WatchedItems.delete_watched_item(watched_item) do
      send_resp(conn, :no_content, "")
    end
  end
end
