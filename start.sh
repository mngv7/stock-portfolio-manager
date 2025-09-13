#!/bin/bash
set -euo pipefail

echo "Initializing tables..."

python3 app/services/dynamo/setup_tables.py

echo "Starting container..."

# Start frontend
cd client
npm install
npm run dev &

# Start backend
cd ../
uvicorn main:app --host 0.0.0.0 --port 5000
