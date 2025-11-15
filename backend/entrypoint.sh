#!/bin/bash
set -e

# Simple entrypoint that just executes the command passed to it
# Migrations are run manually using: docker compose run --rm backend-dev alembic upgrade head
exec "$@"
