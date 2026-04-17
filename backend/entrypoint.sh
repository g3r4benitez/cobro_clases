#!/bin/sh
set -e

echo "Running database migrations..."
# With SQLite (DATABASE_URL=sqlite+aiosqlite:///...), this command also creates
# the .db file automatically if it does not exist.
alembic upgrade head

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
