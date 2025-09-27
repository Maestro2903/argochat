#!/bin/bash

# Fixed Open WebUI Development Server Launcher
# This script addresses version conflicts and missing dependencies

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${2:-$BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

cleanup() {
    log "Shutting down servers..." "$YELLOW"
    if [[ -n "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    if [[ -n "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
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

trap cleanup SIGINT SIGTERM

cd "$(dirname "${BASH_SOURCE[0]}")"

log "🚀 Fixed Open WebUI Development Server Launcher" "$GREEN"

# Kill any existing processes on our ports
log "🔄 Killing existing processes on ports 8080, 5173, 5174..." "$YELLOW"
lsof -ti:8080,5173,5174 | xargs kill -9 2>/dev/null || true
sleep 1

# Check and create .env if needed
if [[ ! -f .env ]]; then
    log "Creating .env file from template..." "$YELLOW"
    cp .env.example .env
fi

# Check if y-protocols is installed, install if missing
if ! npm list y-protocols &>/dev/null; then
    log "Installing missing y-protocols dependency..." "$YELLOW"
    source ~/.nvm/nvm.sh && nvm use 22.12.0 && npm install y-protocols --legacy-peer-deps
fi

log "✅ Dependencies check passed" "$GREEN"

# Find the correct Python executable
PYTHON_CMD=""
for cmd in "/Users/shreeshanthr/.pyenv/versions/3.12.0/bin/python" "python3.12" "python3"; do
    if command -v "$cmd" &> /dev/null; then
        if $cmd --version 2>&1 | grep -q "3\.1[12]"; then
            PYTHON_CMD="$cmd"
            log "✅ Found Python: $($cmd --version) at $cmd" "$GREEN"
            break
        fi
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    log "❌ Python 3.11 or 3.12 not found" "$RED"
    exit 1
fi

# Start backend server
log "🚀 Starting backend server with $PYTHON_CMD..." "$BLUE"
(
    cd backend
    $PYTHON_CMD -m uvicorn open_webui.main:app --reload --host 0.0.0.0 --port 8080 2>&1 | \
    while IFS= read -r line; do
        if [[ "$line" != *"INFO"* ]] || [[ "$line" == *"running on"* ]] || [[ "$line" == *"Uvicorn"* ]]; then
            echo -e "${BLUE}[BACKEND]${NC} $line"
        fi
    done
) &
BACKEND_PID=$!

sleep 3

# Start frontend server with correct Node.js version
log "🚀 Starting frontend server with Node.js 22.12.0..." "$BLUE"
(
    export NVM_DIR="$HOME/.nvm"
    [[ -s "$NVM_DIR/nvm.sh" ]] && \. "$NVM_DIR/nvm.sh"
    nvm use 22.12.0 >/dev/null 2>&1

    npm run dev 2>&1 | \
    while IFS= read -r line; do
        # Filter out verbose messages but keep important ones
        if [[ "$line" == *"ready in"* ]] || [[ "$line" == *"Local:"* ]] || [[ "$line" == *"Network:"* ]] || [[ "$line" == *"VITE"* ]]; then
            echo -e "${GREEN}[FRONTEND]${NC} $line"
        elif [[ "$line" == *"ERROR"* ]] || [[ "$line" == *"Error"* ]]; then
            echo -e "${RED}[FRONTEND]${NC} $line"
        elif [[ "$line" != *"Didn't find package"* ]] && [[ "$line" != *"Loading"* ]] && [[ "$line" != *"Loaded"* ]] && [[ "$line" != *"Installing package"* ]]; then
            # Show other non-verbose lines
            if [[ ${#line} -lt 200 ]]; then
                echo -e "${GREEN}[FRONTEND]${NC} $line"
            fi
        fi
    done
) &
FRONTEND_PID=$!

# Wait for servers to start
log "⏳ Waiting for servers to start..." "$YELLOW"
sleep 10

# Check if processes are still running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    log "❌ Backend server failed to start" "$RED"
    cleanup
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    log "❌ Frontend server failed to start" "$RED"
    cleanup
fi

echo ""
log "🎉 Both servers are running successfully!" "$GREEN"
echo ""
echo -e "${GREEN}📱 Access URLs:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:5173/${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:8080/${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""

# Monitor processes
while true; do
    sleep 5
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        log "❌ Backend process died unexpectedly" "$RED"
        cleanup
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        log "❌ Frontend process died unexpectedly" "$RED"
        cleanup
    fi
done