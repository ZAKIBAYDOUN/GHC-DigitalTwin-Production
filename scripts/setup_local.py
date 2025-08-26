#!/usr/bin/env python3
"""
Setup script for GHC Digital Twin local development environment
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("? Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"? Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_digital_roots():
    """Check if digital-roots repository exists"""
    digital_roots_path = Path("C:/Users/zakib/source/repos/ZAKIBAYDOUN/digital-roots")
    if digital_roots_path.exists():
        print(f"? digital-roots found at {digital_roots_path}")
        return True
    else:
        print(f"??  digital-roots not found at {digital_roots_path}")
        print("   The app will run in remote-only mode")
        return False

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("? Virtual environment already exists")
        return True
    
    try:
        print("?? Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("? Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"? Failed to create virtual environment: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    try:
        print("?? Installing requirements...")
        
        # Use the venv pip if it exists
        if os.name == 'nt':  # Windows
            pip_path = Path("venv/Scripts/pip.exe")
        else:  # Unix/macOS
            pip_path = Path("venv/bin/pip")
        
        if pip_path.exists():
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("? Requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"? Failed to install requirements: {e}")
        return False

def setup_env_file():
    """Setup environment configuration"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("? .env file already exists")
        return True
    
    if env_example.exists():
        try:
            shutil.copy(env_example, env_file)
            print("? Created .env from .env.example")
            print("?? Please review and update .env with your specific settings")
            return True
        except Exception as e:
            print(f"? Failed to create .env file: {e}")
            return False
    else:
        print("??  No .env.example found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "static"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"? Directory '{directory}' ready")

def test_server_startup():
    """Test if the server can start"""
    try:
        print("?? Testing server startup...")
        
        # Try to import the main modules
        import fastapi
        import uvicorn
        print("? FastAPI and Uvicorn available")
        
        # Try to import the local server module
        sys.path.insert(0, str(Path.cwd()))
        import local_server
        print("? Local server module imports successfully")
        
        return True
    except ImportError as e:
        print(f"? Import error: {e}")
        return False
    except Exception as e:
        print(f"? Server test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header("GHC Digital Twin - Local Development Setup")
    
    print("?? Checking prerequisites...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check digital-roots repository
    has_local_agent = check_digital_roots()
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("? Failed to set up virtual environment")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("? Failed to install requirements")
        sys.exit(1)
    
    # Setup environment file
    setup_env_file()
    
    # Create directories
    create_directories()
    
    # Test server
    if not test_server_startup():
        print("? Server startup test failed")
        sys.exit(1)
    
    print_header("Setup Complete!")
    
    print("?? Your local development environment is ready!")
    print("\n?? Next steps:")
    print("   1. Review and update .env file with your settings")
    print("   2. Run: python local_server.py")
    print("   3. Or run: run_local.bat (Windows)")
    print("   4. Open: http://localhost:8000")
    
    if not has_local_agent:
        print("\n??  Note: digital-roots repository not found")
        print("   The app will use remote API mode only")
        print("   To enable local agent mode, ensure digital-roots is at:")
        print("   C:\\Users\\zakib\\source\\repos\\ZAKIBAYDOUN\\digital-roots")

if __name__ == "__main__":
    main()