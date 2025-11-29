#!/bin/bash
mkdir -p _letsencrypt
mkdir -p _postgres
mkdir -p _backend_logs

docker run -ti -v "./frontend/vite-project:/app" -w /app node:22-alpine3.20 npm i

docker compose -f ./compose.yaml build && docker compose -f ./compose-dev.yaml up

