#!/bin/sh

echo "🔄 Waiting for PostgreSQL..."

until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  echo "⏳ DB is not ready - wait 5 seconds..."
  sleep 5
done

echo "✅ DB is available!"

echo "🛠 Running Alembic migrations..."
alembic upgrade head || { echo "❌ Alembic migration failed"; exit 1; }

echo "🚀 Starting FastAPI server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
