#!/bin/sh
# migrate command

set -e

echo >&1 "Checking Postgres is up"
until python -c 'from src.infrastructure.repositories.db import DBRepository; exit(not DBRepository().verify_db_connection())'; do
  echo >&2 "Postgres is unavailable"
  sleep 1
done

echo >&2 "Postgres is up"
alembic upgrade head