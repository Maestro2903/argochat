#!/bin/bash

# Generate SSL certificates for development
# This script creates self-signed certificates for HTTPS development

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CERTS_DIR="$PROJECT_ROOT/certs"

# Function to print colored output
log() {
    echo -e "${2:-$BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

log "🔐 Generating SSL certificates for development..." "$GREEN"

# Create certs directory if it doesn't exist
if [[ ! -d "$CERTS_DIR" ]]; then
    log "Creating certs directory..." "$YELLOW"
    mkdir -p "$CERTS_DIR"
fi

# Check if certificates already exist
if [[ -f "$CERTS_DIR/cert.pem" ]] && [[ -f "$CERTS_DIR/key.pem" ]]; then
    log "SSL certificates already exist. Skipping generation." "$YELLOW"
    log "To regenerate, delete the certs/ directory and run this script again." "$BLUE"
    exit 0
fi

# Generate self-signed certificate
log "Generating self-signed certificate..." "$BLUE"
openssl req -x509 -newkey rsa:4096 \
    -keyout "$CERTS_DIR/key.pem" \
    -out "$CERTS_DIR/cert.pem" \
    -days 365 \
    -nodes \
    -subj "/C=US/ST=CA/L=San Francisco/O=FloatChat/OU=Development/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:127.0.0.1,IP:127.0.0.1"

# Set appropriate permissions
chmod 600 "$CERTS_DIR/key.pem"
chmod 644 "$CERTS_DIR/cert.pem"

log "✅ SSL certificates generated successfully!" "$GREEN"
echo ""
log "📁 Certificate files:" "$BLUE"
echo "   Private Key: $CERTS_DIR/key.pem"
echo "   Certificate: $CERTS_DIR/cert.pem"
echo ""
log "⚠️  Note: These are self-signed certificates for development only." "$YELLOW"
log "   Your browser will show a security warning. Click 'Advanced' and 'Proceed to localhost'." "$YELLOW"
echo ""
