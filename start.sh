#!/bin/bash
set -euo pipefail

echo "Initializing buckets and tables..."

# python3 app/services/dynamo/setup_tables.py
# python3 app/services/s3/s3_setup.py

echo "Starting container..."

# Start frontend
cd client
npm install
npm run dev &

# Start backend
cd ../
uvicorn main:app --host 0.0.0.0 --port 5000
