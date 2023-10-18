defmodule SeriesTrackerApiWeb.WatchedItemJSON do
  alias SeriesTrackerApi.WatchedItems.WatchedItem

  @doc """
  Renders a list of watched_items.
  """
  def index(%{watched_items: watched_items}) do
    %{data: for(watched_item <- watched_items, do: data(watched_item))}
  end

  @doc """
  Renders a single watched_item.
  """
  def show(%{watched_item: watched_item}) do
    %{data: data(watched_item)}
  end

  defp data(%WatchedItem{} = watched_item) do
    %{
      id: watched_item.id,
      user_id: watched_item.user_id,
      name: watched_item.name
    }
  end
end
