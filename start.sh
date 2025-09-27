#!/bin/bash

# Render Start Script for ArgoChat
# This script handles starting the appropriate service

set -e

echo "🚀 Starting ArgoChat service..."

# Detect which service to start based on environment
if [[ "$RENDER_SERVICE_NAME" == *"backend"* ]]; then
    echo "🐍 Starting Backend Service on port $PORT..."

    cd backend

    # Run database migrations
    python -m alembic upgrade head 2>/dev/null || echo "⚠️ Migrations skipped (database might not be ready)"

    # Start the backend server
    exec python -m uvicorn open_webui.main:app --host 0.0.0.0 --port $PORT --workers 1

elif [[ "$RENDER_SERVICE_NAME" == *"frontend"* ]]; then
    echo "🌐 Starting Frontend Service on port $PORT..."

    # Start the frontend server
    exec npm run preview -- --host 0.0.0.0 --port $PORT

else
    echo "⚠️ Unknown service type, starting backend by default..."
    cd backend
    exec python -m uvicorn open_webui.main:app --host 0.0.0.0 --port $PORT
fi