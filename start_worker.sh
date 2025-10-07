#!/bin/bash

echo "Starting monte_carlo_worker at $(date)" >&2

source /home/ubuntu/stock-portfolio-manager/venv/bin/activate
export PYTHONPATH=/home/ubuntu/stock-portfolio-manager:$PYTHONPATH

python -u /home/ubuntu/stock-portfolio-manager/app/utils/monte_carlo_worker.py
