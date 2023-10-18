defmodule SeriesTrackerApi.WatchedItems.WatchedItem do
  use Ecto.Schema
  import Ecto.Changeset

  alias SeriesTrackerApi.Users.User

  schema "watched_items" do
    field :name, :string

    belongs_to :user, User, foreign_key: :user_id

    timestamps()
  end

  @doc false
  def changeset(watched_item, attrs) do
    watched_item
    |> cast(attrs, [:user_id, :name])
    |> validate_required([:user_id, :name])
  end
end
