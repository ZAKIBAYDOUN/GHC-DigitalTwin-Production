#!/usr/bin/env python3
"""
GHC Digital Twin - Complete Setup and Startup Script
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("?? GHC DIGITAL TWIN - LIVE SYSTEM SETUP")
    print("=" * 70)
    print("?? Green Hill Canarias Executive AI Dashboard")
    print("?? 10 Specialized AI Agents")
    print("?? LangGraph Deployment Integration")
    print("?? Real-time Executive Insights")
    print("=" * 70)
    print()

def check_api_keys():
    """Check if API keys are properly configured"""
    env_file = Path(".env")
    if not env_file.exists():
        print("? .env file not found!")
        return False
    
    env_content = env_file.read_text()
    
    # Check for placeholder keys
    needs_setup = False
    
    if "sk-your-openai-api-key-here" in env_content:
        print("??  OpenAI API key needs to be configured")
        print("   Get it from: https://platform.openai.com/api-keys")
        needs_setup = True
    
    if "your-langsmith-api-key-here" in env_content:
        print("??  LangSmith API key needs to be configured") 
        print("   Get it from: https://smith.langchain.com/")
        needs_setup = True
    
    if needs_setup:
        print("\n?? Please update your .env file with real API keys")
        print("?? See API_KEYS_SETUP.md for detailed instructions")
        print("\n? Quick setup:")
        print("1. Get OpenAI API key: https://platform.openai.com/api-keys")
        print("2. Get LangSmith API key: https://smith.langchain.com/")
        print("3. Update .env file with your keys")
        print("4. Run this script again")
        return False
    
    print("? API keys configured!")
    return True

def start_system():
    """Start the GHC Digital Twin system"""
    print("?? Starting GHC Digital Twin Live System...")
    print()
    print("?? LangGraph Deployment: https://dgt-1bf5f8c56c9c5dcd9516a1ba62c5ebf1.us.langgraph.app")
    print("?? Real API credentials: LOADED")
    print("?? AI Agents: 10 Executive specialists")
    print("?? Knowledge Base: Green Hill Canarias data")
    print()
    print("?? Server will start at: http://localhost:8000")
    print("?? API Documentation: http://localhost:8000/docs")
    print()
    
    # Start server using uvicorn for production
    try:
        def open_browser():
            time.sleep(4)
            webbrowser.open('http://localhost:8000')
            print("?? Browser opened automatically")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("Starting server with uvicorn...")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "digital_twin_live:app",
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ])
        
    except KeyboardInterrupt:
        print("\n?? Server stopped by user")
    except Exception as e:
        print(f"? Server error: {e}")

def main():
    """Main setup and startup process"""
    print_banner()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("? Python 3.8+ required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        return
    
    print(f"? Python {sys.version.split()[0]}")
    
    # Check if in correct directory
    if not Path("digital_twin_live.py").exists():
        print("? digital_twin_live.py not found!")
        print("Please run this script from the GHC-DigitalTwin-Production directory")
        input("Press Enter to exit...")
        return
    
    print("? Project files found")
    
    # Check API keys
    if not check_api_keys():
        print("\n?? Setup required before starting the live system")
        input("Press Enter to exit...")
        return
    
    # Install/check dependencies
    print("\n?? Checking dependencies...")
    try:
        import fastapi, uvicorn, httpx, pydantic
        print("? Core dependencies available")
    except ImportError as e:
        print(f"?? Installing missing dependency: {e}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "fastapi", "uvicorn[standard]", "httpx", "pydantic", "python-dotenv"
        ])
    
    # Start the system
    print("\n?? All checks passed! Starting live system...")
    input("\nPress Enter to start the GHC Digital Twin...")
    
    start_system()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n?? Setup interrupted")
    except Exception as e:
        print(f"\n?? Setup error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)