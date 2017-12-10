defmodule AllowancesWeb.SessionView do
  use AllowancesWeb, :view

  def render("info.json", %{info: token}) do
    %{access_token: token}
  end
end
