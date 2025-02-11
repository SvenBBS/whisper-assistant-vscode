#!/bin/bash

# Check if brew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is required but not installed. Please install Homebrew first:"
    echo "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
brew install ffmpeg

# Install pyenv if not already installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    brew install pyenv

    # Add pyenv to shell configuration
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
fi

# Install Python 3.10.13
echo "Installing Python 3.10.13..."
pyenv install 3.10.13 || true
pyenv local 3.10.13

echo "Prerequisites installation complete!"
echo "IMPORTANT: Please restart your terminal, then run ./setup-env.sh"
