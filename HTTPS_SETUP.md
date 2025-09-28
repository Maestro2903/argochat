# HTTPS Development Setup

FloatChat now runs with HTTPS enabled for secure development, which is required for:
- Secure API key handling
- Modern browser security features
- WebRTC and other secure APIs

## Automatic Setup

The development server will automatically:
1. Generate self-signed SSL certificates if they don't exist
2. Configure Vite to use HTTPS
3. Start the frontend on `https://localhost:5173`

## Manual Certificate Generation

If you need to regenerate certificates:

```bash
# Remove existing certificates
rm -rf certs/

# Generate new certificates
./scripts/generate-certs.sh
```

## Browser Security Warning

When you first access `https://localhost:5173`, your browser will show a security warning because the certificate is self-signed.

### Chrome/Edge:
1. Click "Advanced"
2. Click "Proceed to localhost (unsafe)"

### Firefox:
1. Click "Advanced"
2. Click "Accept the Risk and Continue"

### Safari:
1. Click "Show Details"
2. Click "visit this website"
3. Click "Visit Website"

## Certificate Details

- **Location**: `certs/cert.pem` and `certs/key.pem`
- **Validity**: 365 days
- **Subject**: CN=localhost
- **Alt Names**: localhost, 127.0.0.1

## Troubleshooting

### Certificate Not Found Error
If you see certificate errors, regenerate them:
```bash
./scripts/generate-certs.sh
```

### Browser Still Shows HTTP
Clear your browser cache and ensure you're accessing `https://localhost:5173` (not `http://`).

### Port Already in Use
If port 5173 is busy, the Vite server will automatically use the next available port (5174, 5175, etc.).

## Production Deployment

For production deployment, use proper SSL certificates from a Certificate Authority (CA) like Let's Encrypt, not self-signed certificates.
