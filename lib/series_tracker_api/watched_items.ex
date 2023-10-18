defmodule SeriesTrackerApi.WatchedItems do
  @moduledoc """
  The WatchedItems context.
  """

  import Ecto.Query, warn: false
  alias SeriesTrackerApi.Repo

  alias SeriesTrackerApi.WatchedItems.WatchedItem

  @doc """
  Returns the list of watched_items.

  ## Examples

      iex> list_watched_items()
      [%WatchedItem{}, ...]

  """
  def list_watched_items do
    Repo.all(WatchedItem)
  end

  @doc """
  Gets a single watched_item.

  Raises if the Watched item does not exist.

  ## Examples

      iex> get_watched_item!(123)
      %WatchedItem{}

  """
  def get_watched_item!(id), do: Repo.get!(WatchedItem, id)

  @doc """
  Creates a watched_item.

  ## Examples

      iex> create_watched_item(%{field: value})
      {:ok, %WatchedItem{}}

      iex> create_watched_item(%{field: bad_value})
      {:error, ...}

  """
  def create_watched_item(attrs \\ %{}) do
    %WatchedItem{}
    |> WatchedItem.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a watched_item.

  ## Examples

      iex> update_watched_item(watched_item, %{field: new_value})
      {:ok, %WatchedItem{}}

      iex> update_watched_item(watched_item, %{field: bad_value})
      {:error, ...}

  """
  def update_watched_item(%WatchedItem{} = watched_item, attrs) do
    watched_item
    |> WatchedItem.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a WatchedItem.

  ## Examples

      iex> delete_watched_item(watched_item)
      {:ok, %WatchedItem{}}

      iex> delete_watched_item(watched_item)
      {:error, ...}

  """
  def delete_watched_item(%WatchedItem{} = watched_item) do
    Repo.delete(watched_item)
  end

  @doc """
  Returns a data structure for tracking watched_item changes.

  ## Examples

      iex> change_watched_item(watched_item)
      %Todo{...}

  """
  def change_watched_item(%WatchedItem{} = watched_item, attrs \\ %{}) do
    WatchedItem.changeset(watched_item, attrs)
  end
end
