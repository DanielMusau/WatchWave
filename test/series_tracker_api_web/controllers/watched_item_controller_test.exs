defmodule SeriesTrackerApiWeb.WatchedItemControllerTest do
  use SeriesTrackerApiWeb.ConnCase

  import SeriesTrackerApi.WatchedItemsFixtures

  alias SeriesTrackerApi.WatchedItems.WatchedItem

  @create_attrs %{
    series_name: "some series_name",
    user_id: 42
  }
  @update_attrs %{
    series_name: "some updated series_name",
    user_id: 43
  }
  @invalid_attrs %{series_name: nil, user_id: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all watched_items", %{conn: conn} do
      conn = get(conn, ~p"/api/watched_items")
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create watched_item" do
    test "renders watched_item when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/api/watched_items", watched_item: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, ~p"/api/watched_items/#{id}")

      assert %{
               "id" => ^id,
               "series_name" => "some series_name",
               "user_id" => 42
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/api/watched_items", watched_item: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update watched_item" do
    setup [:create_watched_item]

    test "renders watched_item when data is valid", %{conn: conn, watched_item: %WatchedItem{id: id} = watched_item} do
      conn = put(conn, ~p"/api/watched_items/#{watched_item}", watched_item: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, ~p"/api/watched_items/#{id}")

      assert %{
               "id" => ^id,
               "series_name" => "some updated series_name",
               "user_id" => 43
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, watched_item: watched_item} do
      conn = put(conn, ~p"/api/watched_items/#{watched_item}", watched_item: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete watched_item" do
    setup [:create_watched_item]

    test "deletes chosen watched_item", %{conn: conn, watched_item: watched_item} do
      conn = delete(conn, ~p"/api/watched_items/#{watched_item}")
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, ~p"/api/watched_items/#{watched_item}")
      end
    end
  end

  defp create_watched_item(_) do
    watched_item = watched_item_fixture()
    %{watched_item: watched_item}
  end
end
