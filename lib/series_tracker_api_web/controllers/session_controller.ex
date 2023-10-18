defmodule SeriesTrackerApiWeb.SessionController do
  use SeriesTrackerApiWeb, :controller

  alias SeriesTrackerApi.{Users, Users.User, Users.Guardian}
  import Plug.Conn

  def new(conn, _) do
    _changeset = Users.change_user(%User{})
    maybe_user = Guardian.Plug.current_resource(conn)
    if maybe_user do
      redirect(conn, to: "/protected")
    else
      conn
    end
  end

  def login(conn, %{"user" => %{"email" => email, "password" => password_hash}}) do
    case Users.authenticate_user(email, password_hash) do
      {:ok, _user} ->
        conn
        |> put_status(200)
        |> put_resp_header("content-type", "application/json")
        |> json_response(%{message: "Welcome Back!"})

      {:error, _} ->
        conn
        |> put_status(:unauthorized)
        |> put_resp_header("content-type", "application/json")
        |> json_response(%{message: "Invalid Username or Password"})
    end
  end

  defp json_response(conn, data) do
    conn
    |> put_resp_content_type("application/json")
    |> send_resp(200, Jason.encode!(data))
  end

  def logout(conn, _) do
    conn
    |> Guardian.Plug.sign_out() #This module's full name is Auth.UserManager.Guardian.Plug,
    |> redirect(to: "/login")   #and the arguments specified in the Guardian.Plug.sign_out()
  end                           #docs are not applicable here

  # defp login_reply({:ok, user}, conn) do
  #   conn
  #   |> fetch_session()
  #   |> fetch_flash()
  #   |> put_flash(:info, "Welcome back!")
  #   |> Guardian.Plug.sign_in(user)
  #   |> redirect(to: "/protected")
  # end

  # defp login_reply({:error, reason}, conn) do
  #   conn
  #   |> fetch_session()
  #   |> fetch_flash()
  #   |> put_flash(:error, to_string(reason))
  #   |> new(%{})
  # end

end
