defmodule SeriesTrackerApi.WatchedItemsTest do
  use SeriesTrackerApi.DataCase

  alias SeriesTrackerApi.WatchedItems

  describe "watched_items" do
    alias SeriesTrackerApi.WatchedItems.WatchedItem

    import SeriesTrackerApi.WatchedItemsFixtures

    @invalid_attrs %{series_name: nil, user_id: nil}

    test "list_watched_items/0 returns all watched_items" do
      watched_item = watched_item_fixture()
      assert WatchedItems.list_watched_items() == [watched_item]
    end

    test "get_watched_item!/1 returns the watched_item with given id" do
      watched_item = watched_item_fixture()
      assert WatchedItems.get_watched_item!(watched_item.id) == watched_item
    end

    test "create_watched_item/1 with valid data creates a watched_item" do
      valid_attrs = %{series_name: "some series_name", user_id: 42}

      assert {:ok, %WatchedItem{} = watched_item} = WatchedItems.create_watched_item(valid_attrs)
      assert watched_item.series_name == "some series_name"
      assert watched_item.user_id == 42
    end

    test "create_watched_item/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = WatchedItems.create_watched_item(@invalid_attrs)
    end

    test "update_watched_item/2 with valid data updates the watched_item" do
      watched_item = watched_item_fixture()
      update_attrs = %{series_name: "some updated series_name", user_id: 43}

      assert {:ok, %WatchedItem{} = watched_item} = WatchedItems.update_watched_item(watched_item, update_attrs)
      assert watched_item.series_name == "some updated series_name"
      assert watched_item.user_id == 43
    end

    test "update_watched_item/2 with invalid data returns error changeset" do
      watched_item = watched_item_fixture()
      assert {:error, %Ecto.Changeset{}} = WatchedItems.update_watched_item(watched_item, @invalid_attrs)
      assert watched_item == WatchedItems.get_watched_item!(watched_item.id)
    end

    test "delete_watched_item/1 deletes the watched_item" do
      watched_item = watched_item_fixture()
      assert {:ok, %WatchedItem{}} = WatchedItems.delete_watched_item(watched_item)
      assert_raise Ecto.NoResultsError, fn -> WatchedItems.get_watched_item!(watched_item.id) end
    end

    test "change_watched_item/1 returns a watched_item changeset" do
      watched_item = watched_item_fixture()
      assert %Ecto.Changeset{} = WatchedItems.change_watched_item(watched_item)
    end
  end
end
