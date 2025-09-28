#!/usr/bin/env python3
"""
FLOAT CHAT Development Server Manager

This script starts both the frontend and backend servers concurrently,
with proper environment setup and graceful shutdown handling.
"""

import os
import sys
import subprocess
import signal
import time
import threading
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ServerManager:
    def __init__(self):
        self.frontend_process = None
        self.backend_process = None
        self.project_root = Path(__file__).parent

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def log(self, message, color=Colors.CYAN):
        timestamp = time.strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Colors.END}")

    def check_dependencies(self):
        """Check if required dependencies are installed"""
        self.log("🔍 Checking dependencies...", Colors.YELLOW)

        # Kill any existing processes on our ports
        self.log("🔄 Checking for existing processes on ports 8080 and 5173...", Colors.YELLOW)
        try:
            subprocess.run(['bash', '-c', 'lsof -ti:8080,5173,5174 | xargs kill -9 2>/dev/null || true'],
                         cwd=self.project_root, timeout=10)
        except:
            pass

        # Check Node.js version - prefer nvm managed version
        try:
            # Try to use nvm managed Node.js
            result = subprocess.run(['bash', '-c', 'source ~/.nvm/nvm.sh && nvm use 22.12.0 && node --version'],
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                node_version = result.stdout.strip()
                self.log(f"✅ Node.js (via nvm): {node_version}", Colors.GREEN)
            else:
                # Fallback to system Node.js
                result = subprocess.run(['node', '--version'],
                                      capture_output=True, text=True, cwd=self.project_root)
                node_version = result.stdout.strip()
                # Check if version is compatible
                if 'v23.' in node_version:
                    self.log(f"⚠️  Node.js {node_version} detected - forcing switch to v22.12.0", Colors.YELLOW)
                else:
                    self.log(f"✅ Node.js: {node_version}", Colors.GREEN)
        except FileNotFoundError:
            self.log("❌ Node.js not found. Please install Node.js 22.x.x", Colors.RED)
            return False

        # Check npm
        try:
            result = subprocess.run(['npm', '--version'],
                                  capture_output=True, text=True, cwd=self.project_root)
            npm_version = result.stdout.strip()
            self.log(f"✅ npm: {npm_version}", Colors.GREEN)
        except FileNotFoundError:
            self.log("❌ npm not found", Colors.RED)
            return False

        # Check Python - try different versions
        python_cmd = None
        for cmd in ['python3.12', '/Users/shreeshanthr/.pyenv/versions/3.12.0/bin/python', 'python3']:
            try:
                result = subprocess.run([cmd, '--version'],
                                      capture_output=True, text=True, cwd=self.project_root)
                if result.returncode == 0:
                    python_version = result.stdout.strip()
                    if '3.12' in python_version:
                        python_cmd = cmd
                        self.log(f"✅ Python: {python_version} ({cmd})", Colors.GREEN)
                        break
                    elif '3.11' in python_version:
                        python_cmd = cmd
                        self.log(f"✅ Python: {python_version} ({cmd})", Colors.GREEN)
                        break
            except FileNotFoundError:
                continue

        if not python_cmd:
            self.log("❌ Python 3.11+ not found. Please install Python 3.11 or 3.12", Colors.RED)
            return False

        # Store the working Python command
        self.python_cmd = python_cmd

        # Check if node_modules exists
        if not (self.project_root / "node_modules").exists():
            self.log("❌ node_modules not found. Run 'npm install --legacy-peer-deps' first", Colors.RED)
            return False

        # Check if .env exists
        if not (self.project_root / ".env").exists():
            self.log("⚠️  .env file not found. Creating from .env.example...", Colors.YELLOW)
            try:
                subprocess.run(['cp', '.env.example', '.env'],
                             cwd=self.project_root, check=True)
                self.log("✅ Created .env file", Colors.GREEN)
            except subprocess.CalledProcessError:
                self.log("❌ Failed to create .env file", Colors.RED)
                return False

        return True

    def setup_environment(self):
        """Setup environment variables and paths"""
        env = os.environ.copy()

        # Add project root to Python path
        env['PYTHONPATH'] = str(self.project_root / 'backend')

        # Set Node version using nvm if available
        nvm_dir = os.path.expanduser('~/.nvm')
        if os.path.exists(nvm_dir):
            nvm_script = os.path.join(nvm_dir, 'nvm.sh')
            if os.path.exists(nvm_script):
                env['NVM_DIR'] = nvm_dir

        return env

    def start_backend(self, env):
        """Start the backend server"""
        self.log("🚀 Starting backend server...", Colors.BLUE)

        backend_cmd = [
            self.python_cmd, '-m', 'uvicorn',
            'open_webui.main:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', '8080'
        ]

        try:
            self.backend_process = subprocess.Popen(
                backend_cmd,
                cwd=self.project_root / 'backend',
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Start thread to monitor backend output
            backend_thread = threading.Thread(
                target=self.monitor_process,
                args=(self.backend_process, "BACKEND", Colors.BLUE)
            )
            backend_thread.daemon = True
            backend_thread.start()

            self.log("✅ Backend server started on http://0.0.0.0:8080", Colors.GREEN)

        except Exception as e:
            self.log(f"❌ Failed to start backend: {e}", Colors.RED)
            return False

        return True

    def start_frontend(self, env):
        """Start the frontend development server"""
        self.log("🚀 Starting frontend server...", Colors.BLUE)

        # Use nvm to ensure correct Node.js version and install missing deps if needed
        frontend_cmd = [
            'bash', '-c',
            'source ~/.nvm/nvm.sh && nvm use 22.12.0 && npm run dev'
        ]

        try:
            self.frontend_process = subprocess.Popen(
                frontend_cmd,
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Start thread to monitor frontend output
            frontend_thread = threading.Thread(
                target=self.monitor_process,
                args=(self.frontend_process, "FRONTEND", Colors.CYAN)
            )
            frontend_thread.daemon = True
            frontend_thread.start()

            # Wait a bit for frontend to start
            time.sleep(3)

            self.log("✅ Frontend server starting... (will be available shortly)", Colors.GREEN)

        except Exception as e:
            self.log(f"❌ Failed to start frontend: {e}", Colors.RED)
            return False

        return True

    def monitor_process(self, process, name, color):
        """Monitor process output and display it with colored prefix"""
        while process.poll() is None:
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line:
                        # Filter out some verbose output
                        if any(skip in line.lower() for skip in ['warning:', 'didn\'t find package']):
                            continue

                        # Highlight important messages
                        if 'ready in' in line.lower() or 'running on' in line.lower():
                            print(f"{Colors.BOLD}{color}[{name}] {line}{Colors.END}")
                        elif 'error' in line.lower():
                            print(f"{Colors.RED}[{name}] {line}{Colors.END}")
                        else:
                            print(f"{color}[{name}] {line}{Colors.END}")
            except:
                break

    def wait_for_servers(self):
        """Wait for both servers to be ready"""
        self.log("⏳ Waiting for servers to be ready...", Colors.YELLOW)

        # Give servers time to start
        time.sleep(5)

        # Check if processes are still running
        if self.backend_process and self.backend_process.poll() is not None:
            self.log("❌ Backend process exited unexpectedly", Colors.RED)
            return False

        if self.frontend_process and self.frontend_process.poll() is not None:
            self.log("❌ Frontend process exited unexpectedly", Colors.RED)
            return False

        # Display access URLs
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Both servers are running!{Colors.END}")
        print(f"\n{Colors.BOLD}Access URLs:{Colors.END}")
        print(f"  Frontend: {Colors.CYAN}http://localhost:5173/{Colors.END}")
        print(f"  Backend:  {Colors.BLUE}http://localhost:8080/{Colors.END}")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop both servers{Colors.END}\n")

        return True

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log("🛑 Shutting down servers...", Colors.YELLOW)
        self.shutdown()

    def shutdown(self):
        """Gracefully shutdown both servers"""
        if self.frontend_process:
            self.log("Stopping frontend server...", Colors.YELLOW)
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()

        if self.backend_process:
            self.log("Stopping backend server...", Colors.YELLOW)
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()

        self.log("✅ Servers stopped", Colors.GREEN)
        sys.exit(0)

    def run(self):
        """Main execution method"""
        print(f"{Colors.BOLD}{Colors.GREEN}FLOAT CHAT Development Server Manager{Colors.END}")
        print(f"{Colors.CYAN}Starting both frontend and backend servers...{Colors.END}\n")

        # Check dependencies
        if not self.check_dependencies():
            sys.exit(1)

        # Setup environment
        env = self.setup_environment()

        # Start backend server
        if not self.start_backend(env):
            sys.exit(1)

        # Wait a bit for backend to initialize
        time.sleep(2)

        # Start frontend server
        if not self.start_frontend(env):
            self.shutdown()
            sys.exit(1)

        # Wait for servers to be ready
        if not self.wait_for_servers():
            self.shutdown()
            sys.exit(1)

        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)

                # Check if processes are still alive
                if self.backend_process and self.backend_process.poll() is not None:
                    self.log("❌ Backend process died", Colors.RED)
                    break

                if self.frontend_process and self.frontend_process.poll() is not None:
                    self.log("❌ Frontend process died", Colors.RED)
                    break

        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

if __name__ == "__main__":
    manager = ServerManager()
    manager.run()