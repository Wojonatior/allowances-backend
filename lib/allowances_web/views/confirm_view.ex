defmodule AllowancesWeb.ConfirmView do
  use AllowancesWeb, :view

  def render("info.json", %{info: message}) do
    %{info: %{detail: message}}
  end
end
