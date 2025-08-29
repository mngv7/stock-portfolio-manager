#!/bin/bash
set -e

echo "Starting container..."

# Pass API URL to frontend build
cd client
export VITE_API_URL=${VITE_API_URL:-http://localhost:5000}
npm install
npm run dev &

cd ../
uvicorn main:app --host 0.0.0.0 --port 5000
