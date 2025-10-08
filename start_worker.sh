#!/bin/bash

echo "Starting monte_carlo_worker at $(date)"

source /home/ubuntu/stock-portfolio-manager/venv/bin/activate

export PYTHONPATH=/home/ubuntu/stock-portfolio-manager:$PYTHONPATH

python /home/ubuntu/stock-portfolio-manager/app/utils/monte_carlo_worker.py