#!/bin/bash

docker run -ti -v "./frontend/vite-project:/app" -w /app node:22-alpine3.20 npm install json-server

docker run -p 3000:3000 -ti -v "./frontend/vite-project:/app" -w /app node:22-alpine3.20 node_modules/.bin/json-server db.json
