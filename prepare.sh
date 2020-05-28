#!/usr/bin/env bash
command -v docker-compose >/dev/null 2>&1 || { echo >&2 "This script requires `docker-compose` but it's not installed.  Aborting."; exit 1; }
docker-compose build
docker-compose up -d postgres

export PGPASSWORD=bank-rest-api

until docker-compose exec -T postgres psql -U bank-rest-api bank-rest-api -c "select 1" > /dev/null 2>&1; do
  echo "Waiting for postgres server..."
  sleep 1
done

docker-compose exec -T postgres psql -U bank-rest-api < ./schema.sql

echo "Done."
