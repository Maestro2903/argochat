#!/bin/bash

# Open WebUI Development Environment Setup Script
# This script sets up the correct Node.js and Python versions for development

set -e

echo "🚀 Setting up Open WebUI development environment..."

# Check if nvm is installed
if ! command -v nvm &> /dev/null; then
    echo "📦 Installing nvm (Node Version Manager)..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install and use the required Node.js version
echo "📦 Installing Node.js v22.12.0..."
nvm install 22.12.0
nvm use 22.12.0

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "🐍 Installing pyenv (Python Version Manager)..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install pyenv
        else
            echo "❌ Homebrew not found. Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        # Linux
        curl https://pyenv.run | bash
    fi

    # Add pyenv to PATH
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

    # Load pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# Install and set Python version
echo "🐍 Installing Python 3.12.8..."
pyenv install 3.12.8
pyenv local 3.12.8

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Review and update .env file with your configuration"
echo "2. Run 'npm run dev' to start development server"
echo "3. Run 'python -m uvicorn backend.open_webui:app --reload' to start backend"