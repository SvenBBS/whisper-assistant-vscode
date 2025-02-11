#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if venv exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please ensure the virtual environment is set up properly."
    exit 1
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

# Check and install dependencies if needed
echo "📦 Checking dependencies..."
if ! pip freeze | grep -q "fastapi"; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies!"
        deactivate
        exit 1
    fi
fi

echo "🚀 Starting Whisper Assistant API server..."
# Start the FastAPI server using uvicorn
# Host on 0.0.0.0 to allow external access on port 4444
uvicorn main:app --host 0.0.0.0 --port 4444 --reload

# The script will stay running until the server is stopped with Ctrl+C
# When the server stops, deactivate the virtual environment
deactivate
