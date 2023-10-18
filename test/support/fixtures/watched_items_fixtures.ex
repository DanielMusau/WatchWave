defmodule SeriesTrackerApi.WatchedItemsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `SeriesTrackerApi.WatchedItems` context.
  """

  @doc """
  Generate a watched_item.
  """
  def watched_item_fixture(attrs \\ %{}) do
    {:ok, watched_item} =
      attrs
      |> Enum.into(%{
        series_name: "some series_name",
        user_id: 42
      })
      |> SeriesTrackerApi.WatchedItems.create_watched_item()

    watched_item
  end
end
