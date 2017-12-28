defmodule AllowancesWeb.UserResolver do
  alias Allowances.Accounts

  def all_users(_root, _args, _info) do
    users = Accounts.list_users()
    {:ok, users}
  end

  def user(_root, %{id: id}, _info) do
    user = Accounts.get(id)
    {:ok, user}
  end
end