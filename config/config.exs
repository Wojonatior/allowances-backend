# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# General application configuration
config :allowances,
  ecto_repos: [Allowances.Repo]

# Configures the endpoint
config :allowances, AllowancesWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "PdwVp6gfMocynq1SqLVvECUwN1CFLa2f+xOhNvBKyS4HdPRen5mGpWShRzcENXhX",
  render_errors: [view: AllowancesWeb.ErrorView, accepts: ~w(json)],
  pubsub: [name: Allowances.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Phauxth authentication configuration
config :phauxth,
  token_salt: "ZcmI43Qe",
  endpoint: AllowancesWeb.Endpoint

# Mailer configuration
config :allowances, Allowances.Mailer,
  adapter: Bamboo.LocalAdapter

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
