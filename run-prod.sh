#!/bin/bash
mkdir -p _letsencrypt
mkdir -p _postgres
mkdir -p _backend_logs
docker compose -f ./compose.yaml build && docker compose -f ./compose.yaml --env-file .env.prod up -d
