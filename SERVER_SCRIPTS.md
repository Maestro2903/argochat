# Server Management Scripts

This directory contains scripts to easily run both the frontend and backend servers concurrently.

## Available Scripts

### 1. `run_servers.py` (Recommended)
A comprehensive Python script with advanced features:

```bash
python3 run_servers.py
```

**Features:**
- ✅ Dependency checking (Node.js, Python, npm packages)
- ✅ Automatic environment setup
- ✅ Colored output with timestamps
- ✅ Graceful shutdown handling
- ✅ Process monitoring and auto-restart detection
- ✅ Filtered output (removes verbose pyodide messages)
- ✅ Creates .env file if missing

### 2. `start-dev.sh`
A simpler bash script for quick development:

```bash
./start-dev.sh
```

**Features:**
- ✅ Quick startup
- ✅ Colored output
- ✅ Basic process monitoring
- ✅ Graceful shutdown
- ✅ Creates .env file if missing

## Usage

### Quick Start
```bash
# Make sure dependencies are installed
npm install --legacy-peer-deps

# Run the comprehensive Python script
python3 run_servers.py

# OR run the simple bash script
./start-dev.sh
```

### What the Scripts Do

1. **Check Dependencies**: Verify Node.js 22.x, Python 3.12, and npm packages
2. **Create .env**: Copy from .env.example if needed
3. **Start Backend**: Launch FastAPI server on port 8080
4. **Start Frontend**: Launch Vite dev server on port 5173
5. **Monitor**: Watch both processes and handle crashes
6. **Cleanup**: Gracefully shutdown on Ctrl+C

### Access URLs

Once both servers are running:
- **Frontend**: http://localhost:5173/
- **Backend API**: http://localhost:8080/

### Troubleshooting

**Node.js Version Issues:**
```bash
# Install nvm and correct Node.js version
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 22.12.0
nvm use 22.12.0
```

**Python Version Issues:**
```bash
# Install Python 3.12 (macOS with Homebrew)
brew install python@3.12

# Install Python dependencies
python3.12 -m pip install -r backend/requirements.txt
```

**Dependencies Not Installed:**
```bash
# Install frontend dependencies
npm install --legacy-peer-deps

# Install backend dependencies
python3.12 -m pip install -r backend/requirements.txt
```

**Port Already in Use:**
- Stop existing servers: `lsof -ti:8080,5173 | xargs kill -9`
- Or modify ports in the scripts

### Manual Commands

If you prefer to run servers manually:

```bash
# Terminal 1 - Backend
cd backend
python3.12 -m uvicorn open_webui.main:app --reload --host 0.0.0.0 --port 8080

# Terminal 2 - Frontend
source ~/.nvm/nvm.sh && nvm use 22.12.0
npm run dev
```

## Script Comparison

| Feature | run_servers.py | start-dev.sh |
|---------|----------------|--------------|
| Dependency Check | ✅ Comprehensive | ✅ Basic |
| Error Handling | ✅ Advanced | ✅ Basic |
| Output Filtering | ✅ Smart filtering | ✅ Basic filtering |
| Process Monitoring | ✅ Advanced | ✅ Basic |
| Auto-restart | ❌ | ❌ |
| Setup Complexity | Simple to use | Very simple |

## Development Workflow

1. **First Time Setup**: Run `./dev-setup.sh` (automated setup)
2. **Daily Development**: Use `python3 run_servers.py`
3. **Quick Testing**: Use `./start-dev.sh`
4. **Production Build**: Use `npm run build`

Both scripts will handle the environment setup and start both servers with a single command!