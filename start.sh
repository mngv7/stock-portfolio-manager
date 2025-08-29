#!/bin/bash

APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8080"

echo "Starting server"
cd /client
npm install
npm run dev
cd ..
uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT"
