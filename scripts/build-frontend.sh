#!/bin/bash
# FLOAT CHAT Frontend Build Script for Render.com
# Optimized for production deployment

set -e

echo "🚀 Starting FLOAT CHAT Frontend Build Process..."

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

# Set Node.js environment
export NODE_ENV=production
export NODE_OPTIONS="--max-old-space-size=4096"

# Check Node.js version
NODE_VERSION=$(node --version)
log "Using Node.js: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v22\. ]]; then
    warn "Recommended Node.js version is 22.x.x, current: $NODE_VERSION"
fi

# Check npm version
NPM_VERSION=$(npm --version)
log "Using npm: $NPM_VERSION"

# Clean previous builds
log "Cleaning previous build artifacts..."
rm -rf build/
rm -rf .svelte-kit/
rm -rf node_modules/.cache/

# Install dependencies with legacy peer deps flag
log "Installing dependencies..."
npm ci --legacy-peer-deps --prefer-offline --no-audit

# Fetch Pyodide dependencies
log "Fetching Pyodide dependencies..."
npm run pyodide:fetch

# Run SvelteKit checks
log "Running SvelteKit sync and type checks..."
npm run check

# Build the application
log "Building application for production..."
npm run build

# Verify build output
if [[ ! -d "build" ]]; then
    error "Build directory not found! Build failed."
    exit 1
fi

if [[ ! -f "build/index.js" ]]; then
    error "Build output missing! Build may have failed."
    exit 1
fi

# Check build size
BUILD_SIZE=$(du -sh build | cut -f1)
log "Build completed successfully! Size: $BUILD_SIZE"

# List critical build files
log "Build contents:"
ls -la build/

log "✅ Frontend build complete and ready for deployment!"