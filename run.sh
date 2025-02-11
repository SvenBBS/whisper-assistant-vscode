#!/bin/bash

# Clear PYTHONPATH to avoid interference from system packages
export PYTHONPATH=""

# Activate virtual environment
source venv/bin/activate

# Run the FastAPI server with uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 4444
