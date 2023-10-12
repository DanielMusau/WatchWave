defmodule SeriesTrackerApi.WatchedItems.WatchedItem do
  use Ecto.Schema
  import Ecto.Changeset

  schema "watched_items" do
    field :series_name, :string
    field :user_id, :integer

    timestamps()
  end

  @doc false
  def changeset(watched_item, attrs) do
    watched_item
    |> cast(attrs, [:user_id, :series_name])
    |> validate_required([:user_id, :series_name])
  end
end
