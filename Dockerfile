# Use the official Elixir image with Alpine Linux
FROM hexpm/elixir:1.14.2-erlang-24.1.2-alpine-3.14.2

# Set the environment variables
ENV MIX_ENV=prod

# Install build tools (including make)
RUN apk update && \
    apk add --no-cache build-base

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install Hex and Rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Install mix dependencies
RUN mix deps.get

# Compile the application
RUN mix compile

# Build the static assets and generate cache manifest
RUN mix phx.digest

# Run database migrations (if applicable)
# RUN mix ecto.migrate

# Build the release
RUN mix release

# Expose the necessary port (if applicable)
# EXPOSE <port>

# Set the entrypoint command for the release
CMD ["./_build/prod/rel/series_tracker_api/bin/series_tracker_api", "start"]