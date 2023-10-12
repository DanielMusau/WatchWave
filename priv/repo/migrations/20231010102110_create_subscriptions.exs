defmodule SeriesTrackerApi.Repo.Migrations.CreateSubscriptions do
  use Ecto.Migration

  def change do
    create table(:subscriptions) do
      add :user_id, :integer
      add :series_name, :string

      timestamps()
    end
  end
end
