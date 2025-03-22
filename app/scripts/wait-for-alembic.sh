#!/bin/sh

# wait-for-alembic.sh
set -e

host="$1"
shift
cmd="$@"


set -e

echo >&1 "Checking Postgres is up"
until python -c 'from src.infrastructure.repositories.db import DBRepository; exit(not DBRepository().verify_db_connection())'; do
  echo >&2 "Postgres is unavailable"
  sleep 1
done

echo >&2 "Postgres is up"

# Function to check if the alembic_version table has at least one version entry
check_alembic_migration() {
  PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT 1 FROM alembic_version LIMIT 1" | tr -d '[:space:]'
}

# Wait until the alembic_version table is not empty (indicating migrations have been applied)
until [[ "$(check_alembic_migration)" == "1" ]]; do
  >&2 echo "Waiting for Alembic migrations to complete..."
  sleep 1
done

>&2 echo "Alembic migrations have completed. Proceeding with command."
exec $cmd