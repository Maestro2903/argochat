#!/bin/bash

# FLOAT CHAT Development Server Launcher
# This script starts both frontend and backend servers concurrently

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
log() {
    echo -e "${2:-$BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

# Function to cleanup processes on exit
cleanup() {
    log "Shutting down servers..." "$YELLOW"

    # Kill background processes
    if [[ -n "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi

    if [[ -n "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi

    # Wait a bit then force kill if necessary
    sleep 2

    if [[ -n "$FRONTEND_PID" ]] && kill -0 $FRONTEND_PID 2>/dev/null; then
        kill -9 $FRONTEND_PID 2>/dev/null || true
    fi

    if [[ -n "$BACKEND_PID" ]] && kill -0 $BACKEND_PID 2>/dev/null; then
        kill -9 $BACKEND_PID 2>/dev/null || true
    fi

    log "Servers stopped" "$GREEN"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Change to project directory
cd "$PROJECT_ROOT"

log "🚀 FLOAT CHAT Development Server Launcher" "$GREEN"
log "Starting both frontend and backend servers..." "$BLUE"

# Check dependencies
log "Checking dependencies..." "$YELLOW"

# Check if .env exists
if [[ ! -f .env ]]; then
    log "Creating .env file from template..." "$YELLOW"
    cp .env.example .env
fi

# Check if SSL certificates exist, generate if needed
if [[ ! -f certs/cert.pem ]] || [[ ! -f certs/key.pem ]]; then
    log "SSL certificates not found. Generating..." "$YELLOW"
    ./scripts/generate-certs.sh
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    log "❌ Node.js not found. Please install Node.js 22.x.x" "$RED"
    exit 1
fi

# Check Python
if ! command -v python3.12 &> /dev/null; then
    log "❌ Python 3.12 not found. Please install Python 3.12" "$RED"
    exit 1
fi

# Check node_modules
if [[ ! -d node_modules ]]; then
    log "❌ node_modules not found. Please run 'npm install --legacy-peer-deps'" "$RED"
    exit 1
fi

log "✅ Dependencies check passed" "$GREEN"

# Start backend server in background
log "🚀 Starting backend server..." "$BLUE"
(
    cd backend
    WEBUI_AUTH=true ENABLE_SIGNUP=true python3.12 -m uvicorn open_webui.main:app --reload --host 0.0.0.0 --port 8080 2>&1 | \
    while IFS= read -r line; do
        echo -e "${BLUE}[BACKEND]${NC} $line"
    done
) &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Start frontend server in background
log "🚀 Starting frontend server..." "$BLUE"
(
    # Load nvm and use correct Node.js version
    export NVM_DIR="$HOME/.nvm"
    [[ -s "$NVM_DIR/nvm.sh" ]] && \. "$NVM_DIR/nvm.sh"
    nvm use 22.12.0 >/dev/null 2>&1 || true

    npm run dev 2>&1 | \
    while IFS= read -r line; do
        # Filter out verbose pyodide messages
        if [[ "$line" != *"Didn't find package"* ]] && [[ "$line" != *"Loading"* ]] && [[ "$line" != *"Loaded"* ]]; then
            echo -e "${GREEN}[FRONTEND]${NC} $line"
        fi
    done
) &
FRONTEND_PID=$!

# Wait for servers to initialize
log "⏳ Waiting for servers to start..." "$YELLOW"
sleep 8

# Check if processes are still running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    log "❌ Backend server failed to start" "$RED"
    cleanup
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    log "❌ Frontend server failed to start" "$RED"
    cleanup
fi

# Display success message and URLs
echo ""
log "🎉 Both servers are running successfully!" "$GREEN"
echo ""
echo -e "${GREEN}📱 Access URLs:${NC}"
echo -e "   Frontend: ${BLUE}https://localhost:5173/${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:8080/${NC}"
echo ""
echo -e "${YELLOW}⚠️  HTTPS Note: Your browser will show a security warning for the self-signed certificate.${NC}"
echo -e "${YELLOW}   Click 'Advanced' → 'Proceed to localhost (unsafe)' to continue.${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""

# Keep script running and monitor processes
while true; do
    sleep 5

    # Check if backend is still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        log "❌ Backend process died unexpectedly" "$RED"
        cleanup
    fi

    # Check if frontend is still running
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        log "❌ Frontend process died unexpectedly" "$RED"
        cleanup
    fi
done