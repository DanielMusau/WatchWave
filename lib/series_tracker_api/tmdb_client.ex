defmodule SeriesTrackerApi.TMDbClient do
  import HTTPoison.Base

  def get(path, query_params \\ %{}, options \\ []) do
    base_url = SeriesTrackerApi.TMDbConfig.api_base_url()
    api_key = SeriesTrackerApi.TMDbConfig.api_key()


    headers = [
      {"accept", "application/json"},
      {"Authorization", "Bearer #{api_key}"}
    ]

    query_string = URI.encode_query(query_params)

    full_url = base_url <> path <> "?" <> query_string

    response = HTTPoison.get(full_url, headers, options)

    case response do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} ->
        case Jason.decode(body) do
          {:ok, %{"results" => results}} ->
            {:ok, results}
          _ ->
            {:error, "TMDb API response format is unexpected: #{body}"}
        end

      {:ok, %HTTPoison.Response{status_code: code, body: body}} when code == 401 ->
        {:error, "TMDb API returned a 401 Unauthorized error: #{body}"}

      {:ok, %HTTPoison.Response{status_code: code, body: body}} ->
        {:error, "TMDb API returned status code #{code}: #{body}"}

      {:error, reason} ->
        {:error, reason}
    end
  end
end
