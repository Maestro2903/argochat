# Development Environment Setup

## Version Requirements

Based on the project's dependency files:

- **Node.js**: `>=18.13.0 <=22.x.x` (recommended: 22.12.0)
- **npm**: `>=6.0.0` (comes with Node.js 22.12.0: v10.9.0)
- **Python**: `>= 3.11, < 3.13.0a1` (recommended: 3.12.8)

## Quick Setup

Run the automated setup script:
```bash
./dev-setup.sh
```

## Manual Setup

### 1. Install Node.js (using nvm)
```bash
# Install nvm if not already installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell or run:
source ~/.nvm/nvm.sh

# Install and use the correct Node.js version
nvm install 22.12.0
nvm use 22.12.0
```

### 2. Install Python (using pyenv)
```bash
# Install pyenv (macOS with Homebrew)
brew install pyenv

# Install and set Python version
pyenv install 3.12.8
pyenv local 3.12.8
```

### 3. Install Dependencies
```bash
# Frontend dependencies
npm install --legacy-peer-deps

# Backend dependencies
pip install -r backend/requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
```

## Development Commands

### Frontend Development
```bash
# Start development server (frontend only)
npm run dev

# Start on specific port
npm run dev:5050

# Build for production
npm run build

# Build and watch for changes
npm run build:watch

# Preview production build
npm run preview
```

### Backend Development
```bash
# Start backend server
cd backend
python -m uvicorn open_webui.main:app --reload --host 0.0.0.0 --port 8080

# Or use the provided script
./backend/dev.sh
```

### Full Stack Development
```bash
# Terminal 1 - Frontend
npm run dev

# Terminal 2 - Backend
cd backend && python -m uvicorn open_webui.main:app --reload --host 0.0.0.0 --port 8080
```

### Code Quality
```bash
# Run all linting
npm run lint

# Lint frontend only
npm run lint:frontend

# Lint types
npm run lint:types

# Lint backend
npm run lint:backend

# Format code
npm run format

# Format backend code
npm run format:backend

# Type checking
npm run check

# Type checking with watch
npm run check:watch
```

### Testing
```bash
# Run frontend tests
npm run test:frontend

# Open Cypress for e2e testing
npm run cy:open
```

### Internationalization
```bash
# Parse i18n strings
npm run i18n:parse
```

## Docker Development (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

## Troubleshooting

### Node.js Version Issues
- Ensure you're using Node.js 22.x.x (not 23.x.x or higher)
- Use `nvm use 22.12.0` to switch versions

### Python Version Issues
- Ensure Python version is between 3.11 and 3.13 (exclusive)
- Use `pyenv local 3.12.8` to set project Python version

### Dependency Conflicts
- Use `npm install --legacy-peer-deps` for frontend
- Clear `node_modules` and reinstall if needed: `rm -rf node_modules package-lock.json && npm install --legacy-peer-deps`

### Build Issues
- Run `npm run pyodide:fetch` first if build fails
- Ensure all dependencies are installed
- Check that `.env` file exists with proper configuration

## Project Structure

- `/src` - Frontend Svelte application
- `/backend` - Python FastAPI backend
- `/static` - Static assets
- `/docs` - Documentation
- `/cypress` - E2E tests
- `/scripts` - Build and utility scripts