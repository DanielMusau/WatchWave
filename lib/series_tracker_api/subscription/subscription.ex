defmodule SeriesTrackerApi.Subscription.Subscription do
  use Ecto.Schema
  import Ecto.Changeset

  schema "subscriptions" do
    field :series_name, :string
    field :user_id, :integer

    timestamps()
  end

  @doc false
  def changeset(subscription, attrs) do
    subscription
    |> cast(attrs, [:user_id, :series_name])
    |> validate_required([:user_id, :series_name])
  end
end
