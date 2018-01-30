defmodule AllowancesWeb.Schema do
  use Absinthe.Schema

  alias AllowancesWeb.UserResolver

  object :user do
    field :id, non_null(:id)
    field :email, non_null(:string)
    field :confirmed_at, :string
  end

  query do
    field :user, :user do
      arg :id, :id, description: "Unique user identifier"
      resolve &UserResolver.user/3
    end

    field :users, non_null(list_of(non_null(:user))) do
      resolve &UserResolver.all_users/3
    end
  end
end