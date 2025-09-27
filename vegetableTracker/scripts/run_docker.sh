#!/usr/bin/env bash
set -euo pipefail

# Helper: start docker-compose stack (Postgres + migration)
# Usage: ./scripts/run_docker.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Starting Postgres and applying migrations via docker-compose..."

docker-compose up -d db

# Wait for Postgres to be ready
until docker exec vegtracker-db pg_isready -U vtuser > /dev/null 2>&1; do
  echo "Waiting for Postgres..."
  sleep 1
done

echo "Applying migrations inside a transient container..."
# Run migration file from host mounted migrations directory
docker run --rm --network host -v "$ROOT_DIR/backend/migrations:/migrations:ro" postgres:15 bash -c "until pg_isready -h localhost -p 5432; do sleep 1; done; psql postgresql://vtuser:vtpass@localhost:5432/vegtracker -f /migrations/001_init.sql"

echo "Migrations applied. You can now run the backend with VT_DATABASE_DSN=postgres://vtuser:vtpass@localhost:5432/vegtracker?sslmode=disable"

echo "Tailing postgres logs (ctrl-C to exit)..."
docker logs -f vegtracker-db
