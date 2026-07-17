#!/bin/sh

# exit if any errors are thrown
set -e

# guarantee the DB volume directory exists
mkdir -p /app/data

# create DB/run migrations
.venv/bin/alembic upgrade head

# hand over the control to the program passed as arguments to this script
exec "$@"