defmodule SeriesTrackerApi.Repo.Migrations.CreateWatchedItems do
  use Ecto.Migration

  def change do
    create table(:watched_items) do
      add :user_id, references(:users, on_delete: :nothing), null: false
      add :name, :string, null: false

      timestamps()
    end
  end
end
