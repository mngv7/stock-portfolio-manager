#!/bin/bash
set -e 

echo "Starting container..."

cd client
npm install
npm run dev &

cd ../
uvicorn main:app --host 0.0.0.0 --port 5000
