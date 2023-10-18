defmodule SeriesTrackerApi.SubscriptionsTest do
  use SeriesTrackerApi.DataCase

  alias SeriesTrackerApi.Subscriptions

  describe "subscriptions" do
    alias SeriesTrackerApi.Subscriptions.Subscription

    import SeriesTrackerApi.SubscriptionsFixtures

    @invalid_attrs %{series_name: nil, user_id: nil}

    test "list_subscriptions/0 returns all subscriptions" do
      subscription = subscription_fixture()
      assert Subscriptions.list_subscriptions() == [subscription]
    end

    test "get_subscription!/1 returns the subscription with given id" do
      subscription = subscription_fixture()
      assert Subscriptions.get_subscription!(subscription.id) == subscription
    end

    test "create_subscription/1 with valid data creates a subscription" do
      valid_attrs = %{series_name: "some series_name", user_id: 42}

      assert {:ok, %Subscription{} = subscription} = Subscriptions.create_subscription(valid_attrs)
      assert subscription.series_name == "some series_name"
      assert subscription.user_id == 42
    end

    test "create_subscription/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Subscriptions.create_subscription(@invalid_attrs)
    end

    test "update_subscription/2 with valid data updates the subscription" do
      subscription = subscription_fixture()
      update_attrs = %{series_name: "some updated series_name", user_id: 43}

      assert {:ok, %Subscription{} = subscription} = Subscriptions.update_subscription(subscription, update_attrs)
      assert subscription.series_name == "some updated series_name"
      assert subscription.user_id == 43
    end

    test "update_subscription/2 with invalid data returns error changeset" do
      subscription = subscription_fixture()
      assert {:error, %Ecto.Changeset{}} = Subscriptions.update_subscription(subscription, @invalid_attrs)
      assert subscription == Subscriptions.get_subscription!(subscription.id)
    end

    test "delete_subscription/1 deletes the subscription" do
      subscription = subscription_fixture()
      assert {:ok, %Subscription{}} = Subscriptions.delete_subscription(subscription)
      assert_raise Ecto.NoResultsError, fn -> Subscriptions.get_subscription!(subscription.id) end
    end

    test "change_subscription/1 returns a subscription changeset" do
      subscription = subscription_fixture()
      assert %Ecto.Changeset{} = Subscriptions.change_subscription(subscription)
    end
  end
end
