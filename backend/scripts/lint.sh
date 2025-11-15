#!/bin/sh -e

set -x

# Run ruff linter with auto-fix
ruff check --fix src

# Format code with ruff
ruff format src

