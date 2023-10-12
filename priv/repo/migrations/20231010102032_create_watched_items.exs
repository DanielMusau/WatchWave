defmodule SeriesTrackerApi.Repo.Migrations.CreateWatchedItems do
  use Ecto.Migration

  def change do
    create table(:watched_items) do
      add :user_id, :integer
      add :series_name, :string

      timestamps()
    end
  end
end
