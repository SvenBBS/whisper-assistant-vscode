#!/bin/bash

# Verify we're using Python 3.10.13
PYTHON_VERSION=$(python --version)
if [[ $PYTHON_VERSION != *"3.10.13"* ]]; then
    echo "Error: Python 3.10.13 is required but found $PYTHON_VERSION"
    echo "Please make sure you:"
    echo "1. Ran ./setup-prereqs.sh"
    echo "2. Restarted your terminal"
    echo "3. Are in the correct directory (you should see .python-version file)"
    exit 1
fi

# Deactivate any active virtual environment
if [[ -n $VIRTUAL_ENV ]]; then
    echo "Deactivating existing virtual environment..."
    deactivate
fi

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create Python virtual environment
echo "Creating Python virtual environment..."
python -m venv venv --clear
source venv/bin/activate

# Clear PYTHONPATH to avoid interference from system packages
export PYTHONPATH=""

# Install Python packages
echo "Installing Python packages..."
python -m pip install --upgrade pip

# Install NumPy 1.x first to ensure compatibility
echo "Installing NumPy 1.x..."
python -m pip install --no-cache-dir 'numpy<2.0.0'

# Install PyTorch with specific version for macOS
echo "Installing PyTorch..."
python -m pip install --no-cache-dir torch==2.1.2

# Install remaining packages
echo "Installing other dependencies..."
python -m pip install --no-cache-dir fastapi uvicorn python-multipart more-itertools tqdm numba openai-whisper

# Verify torch installation
echo "Verifying torch installation..."
PYTHONPATH="" python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Pre-download the whisper base model
echo "Downloading whisper base model..."
PYTHONPATH="" python -c "import whisper; whisper.load_model('base')"

echo "Setup complete! To run the server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the server: ./run.sh"
