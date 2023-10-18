defmodule SeriesTrackerApi.SubscriptionsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `SeriesTrackerApi.Subscriptions` context.
  """

  @doc """
  Generate a subscription.
  """
  def subscription_fixture(attrs \\ %{}) do
    {:ok, subscription} =
      attrs
      |> Enum.into(%{
        series_name: "some series_name",
        user_id: 42
      })
      |> SeriesTrackerApi.Subscriptions.create_subscription()

    subscription
  end
end
