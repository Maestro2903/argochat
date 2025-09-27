#!/bin/bash

# Render Build Script for ArgoChat
# This script handles the build process for both frontend and backend

set -e

echo "🚀 Starting ArgoChat build process..."

# Detect which service is being built based on environment
if [[ "$RENDER_SERVICE_NAME" == *"backend"* ]]; then
    echo "📦 Building Backend Service..."

    # Install Python dependencies
    pip install --upgrade pip
    pip install -r backend/requirements.txt

    echo "✅ Backend build complete"

elif [[ "$RENDER_SERVICE_NAME" == *"frontend"* ]]; then
    echo "📦 Building Frontend Service..."

    # Use specific Node.js version
    echo "📋 Using Node.js version: $(node --version)"

    # Install dependencies
    npm install --legacy-peer-deps

    # Fetch Pyodide packages
    npm run pyodide:fetch

    # Build the frontend
    npm run build

    echo "✅ Frontend build complete"

else
    echo "⚠️ Unknown service type, running default build..."

    # Install both dependencies
    pip install --upgrade pip
    pip install -r backend/requirements.txt
    npm install --legacy-peer-deps
    npm run build
fi

echo "🎉 Build process completed successfully!"