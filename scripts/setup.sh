#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  chmod 600 backend/.env
  echo 'Completar APP_KEY y DEVICE_TOKEN en backend/.env antes de continuar.' >&2
  exit 1
fi
docker compose build
docker compose run --rm app php -r "if (!file_exists('/app/storage/database.sqlite')) { touch('/app/storage/database.sqlite'); }"
docker compose run --rm app php artisan migrate --force
docker compose up -d
