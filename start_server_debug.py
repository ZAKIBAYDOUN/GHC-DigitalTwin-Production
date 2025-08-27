#!/usr/bin/env python3
"""
GHC Digital Twin Live System Startup with Debugging
"""
import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    print("="*60)
    print("?? GHC DIGITAL TWIN LIVE SYSTEM STARTUP")
    print("="*60)
    print("?? LangGraph Cloud Integration Active")
    print("?? Real AI Agents Ready")
    print("?? Enhanced Knowledge Base")
    print("="*60)
    print()

def check_dependencies():
    """Check and install required dependencies"""
    print("?? Checking dependencies...")
    
    required_packages = [
        "fastapi", "uvicorn", "python-dotenv", "pydantic", 
        "httpx", "aiofiles", "requests"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"? {package}")
        except ImportError:
            missing.append(package)
            print(f"? {package} - MISSING")
    
    if missing:
        print(f"\n?? Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", *missing
            ])
            print("? All packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"? Failed to install packages: {e}")
            return False
    
    return True

def check_environment():
    """Check environment configuration"""
    print("\n?? Checking environment...")
    
    # Check .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("? .env file not found!")
        return False
    
    print("? .env file found")
    
    # Check for required directories
    dirs = ["data", "logs", "static", "api"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"? Created directory: {dir_name}")
        else:
            print(f"? Directory exists: {dir_name}")
    
    return True

def start_server():
    """Start the Digital Twin server"""
    print("\n?? Starting GHC Digital Twin Live System...")
    print("?? Server will be available at: http://localhost:8000")
    print("?? API Documentation: http://localhost:8000/docs")
    print("?? LangGraph Cloud Integration: ACTIVE")
    print()
    
    try:
        # Import and check the main application
        import digital_twin_live
        print("? Application module imported successfully")
        
        # Start with uvicorn for better error handling
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "digital_twin_live:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
    except ImportError as e:
        print(f"? Failed to import application: {e}")
        print("Trying direct execution...")
        subprocess.run([sys.executable, "digital_twin_live.py"])
        
    except KeyboardInterrupt:
        print("\n?? Server stopped by user")
        
    except Exception as e:
        print(f"? Server error: {e}")
        print("\nTrying alternative startup...")
        subprocess.run([sys.executable, "digital_twin_live.py"])

def main():
    """Main startup process"""
    print_banner()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("? Python 3.8+ required")
        sys.exit(1)
    
    print(f"? Python {sys.version.split()[0]}")
    
    # Check dependencies
    if not check_dependencies():
        print("? Dependency check failed")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("? Environment check failed")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("\n?? All checks passed! Starting server...")
    
    # Start server
    start_server()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n?? Startup error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)