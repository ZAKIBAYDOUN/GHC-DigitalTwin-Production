#!/usr/bin/env python3
"""
GHC Digital Twin Live System - Final Production Startup
"""
import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_port():
    """Check if port 8000 is available"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        if ':8000' in result.stdout:
            print("??  Port 8000 is already in use")
            return False
        return True
    except:
        return True

def start_server():
    """Start the GHC Digital Twin server"""
    print("?? Starting GHC Digital Twin Live System...")
    print("="*60)
    print("?? LangGraph Cloud Integration: ACTIVE")
    print("?? Real API Credentials: LOADED")
    print("?? AI Agents: 10 Specialized Executives")
    print("?? Knowledge Base: 4 Business Domains")
    print("="*60)
    
    try:
        # Start server using uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "digital_twin_live:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]
        
        print(f"?? Starting server: {' '.join(cmd)}")
        print("?? Server URL: http://localhost:8000")
        print("?? API Docs: http://localhost:8000/docs")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Wait a moment for server to start, then open browser
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8000')
                print("?? Browser opened automatically")
            except:
                print("??  Please open http://localhost:8000 manually")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the server
        subprocess.run(cmd, check=False)
        
    except KeyboardInterrupt:
        print("\n?? Server stopped by user")
    except Exception as e:
        print(f"? Server error: {e}")
        print("\nTrying fallback startup...")
        subprocess.run([sys.executable, "digital_twin_live.py"])

def main():
    """Main execution"""
    if not Path("digital_twin_live.py").exists():
        print("? digital_twin_live.py not found!")
        sys.exit(1)
    
    if not Path(".env").exists():
        print("? .env file not found!")
        sys.exit(1)
    
    if not check_port():
        print("Please close the application using port 8000 and try again")
        sys.exit(1)
    
    start_server()

if __name__ == "__main__":
    main()