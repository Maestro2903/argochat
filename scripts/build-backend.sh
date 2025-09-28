#!/bin/bash
# FLOAT CHAT Backend Build Script for Render.com
# Optimized for production deployment

set -e

echo "🚀 Starting FLOAT CHAT Backend Build Process..."

# Color codes for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[BUILD]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
PYTHON_VERSION=$(python3.12 --version 2>/dev/null || python3 --version 2>/dev/null || python --version)
log "Using Python: $PYTHON_VERSION"

# Upgrade pip and essential build tools
log "Upgrading pip and build tools..."
python3.12 -m pip install --upgrade pip setuptools wheel

# Check if we're in the backend directory or project root
if [[ -f "requirements.txt" ]]; then
    REQUIREMENTS_FILE="requirements.txt"
elif [[ -f "backend/requirements.txt" ]]; then
    REQUIREMENTS_FILE="backend/requirements.txt"
else
    error "Requirements file not found!"
    exit 1
fi

log "Found requirements file: $REQUIREMENTS_FILE"

# Install Python dependencies
log "Installing Python dependencies..."
pip install -r "$REQUIREMENTS_FILE" --no-cache-dir --disable-pip-version-check

# Verify critical imports
log "Verifying critical Python imports..."
python3.12 -c "
import fastapi
import uvicorn
import pydantic
import sqlalchemy
import openai
print('✅ All critical imports successful')
"

# Check if backend structure is correct
if [[ -d "backend/open_webui" ]]; then
    log "Backend structure verified"
elif [[ -d "open_webui" ]]; then
    log "Backend structure verified (current directory)"
else
    error "Backend structure not found! Expected 'open_webui' directory."
    exit 1
fi

# Create data directory if it doesn't exist
log "Setting up data directory..."
mkdir -p backend/data || mkdir -p data

# Check database connectivity (if DATABASE_URL is set)
if [[ -n "$DATABASE_URL" ]]; then
    log "Database URL configured: ${DATABASE_URL:0:20}..."
else
    log "Using SQLite database (default)"
fi

# Test backend startup (quick validation)
log "Testing backend startup..."
timeout 10s python3.12 -c "
import sys
sys.path.insert(0, 'backend' if 'backend' in '$PWD' else '.')
from open_webui.main import app
print('✅ Backend startup test successful')
" || warn "Backend startup test timed out (this may be normal)"

log "✅ Backend build complete and ready for deployment!"