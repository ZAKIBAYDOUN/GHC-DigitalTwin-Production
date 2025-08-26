"""
Complete System Verification Test
Tests all deployment options for GHC Digital Twin
"""
import requests
import time
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_header(title):
    print("\n" + "="*50)
    print(f"  {title}")
    print("="*50)

def test_github_pages():
    """Test GitHub Pages deployment"""
    print("?? Testing GitHub Pages deployment...")
    
    try:
        url = "https://zakibaydoun.github.io/GHC-DT/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"? GitHub Pages is live: {url}")
            print(f"   Response size: {len(response.text)} bytes")
            
            # Check for key elements
            if "Green Hill Canarias" in response.text:
                print("? Title found in page")
            if "Digital Twin" in response.text:
                print("? Digital Twin content found")
            if "CEO Digital Twin" in response.text:
                print("? Agent content found")
                
            return True
        else:
            print(f"? GitHub Pages returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"? GitHub Pages test failed: {e}")
        return False

def test_local_server():
    """Test local server if running"""
    print("?? Testing local server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/system/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("? Local server is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Agents: {data.get('agents')}")
            print(f"   Version: {data.get('version')}")
            
            # Test agents endpoint
            agents_response = requests.get("http://localhost:8000/api/agents", timeout=5)
            if agents_response.status_code == 200:
                agents_data = agents_response.json()
                print(f"? Agents endpoint working ({len(agents_data.get('agents', []))} agents)")
            
            return True
        else:
            print(f"? Local server returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("??  Local server not running (this is normal)")
        return False
    except Exception as e:
        print(f"? Local server test failed: {e}")
        return False

def check_files():
    """Check that all necessary files exist"""
    print("?? Checking file structure...")
    
    required_files = [
        "index.html",
        "simple_digital_twin.py", 
        "start_system.bat",
        "run_digital_twin.bat",
        ".github/workflows/deploy.yml",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"? {file_path}")
        else:
            print(f"? {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_startup_scripts():
    """Test that startup scripts are properly formatted"""
    print("?? Checking startup scripts...")
    
    scripts = ["start_system.bat", "run_digital_twin.bat", "run_local.bat"]
    
    for script in scripts:
        if Path(script).exists():
            print(f"? {script} exists")
            
            # Check file is not empty
            content = Path(script).read_text(encoding='utf-8', errors='ignore')
            if len(content) > 100:
                print(f"   Content length: {len(content)} characters")
            else:
                print(f"??  {script} seems too short")
        else:
            print(f"? {script} missing")

def open_demo():
    """Open the demo in browser"""
    print("?? Opening demo in browser...")
    
    try:
        # First try local server
        try:
            requests.get("http://localhost:8000", timeout=2)
            webbrowser.open("http://localhost:8000")
            print("? Opened local server in browser")
            return
        except:
            pass
        
        # Fallback to GitHub Pages
        webbrowser.open("https://zakibaydoun.github.io/GHC-DT/")
        print("? Opened GitHub Pages in browser")
        
    except Exception as e:
        print(f"? Could not open browser: {e}")

def main():
    print_header("GHC DIGITAL TWIN - COMPLETE SYSTEM TEST")
    
    print("?? Green Hill Canarias Digital Twin")
    print("   Sophisticated AI-powered startup dashboard")
    print("   Testing all deployment options...\n")
    
    # Test file structure
    files_ok = check_files()
    
    # Test startup scripts
    test_startup_scripts()
    
    # Test GitHub Pages
    github_ok = test_github_pages()
    
    # Test local server
    local_ok = test_local_server()
    
    print_header("DEPLOYMENT STATUS SUMMARY")
    
    # Summary
    print(f"?? File Structure:    {'? PASS' if files_ok else '? ISSUES'}")
    print(f"?? GitHub Pages:      {'? LIVE' if github_ok else '? OFFLINE'}")  
    print(f"?? Local Server:      {'? RUNNING' if local_ok else '??  STOPPED'}")
    
    print("\n?? AVAILABLE DEPLOYMENT OPTIONS:")
    
    if github_ok:
        print("? Production:  https://zakibaydoun.github.io/GHC-DT/")
    
    if local_ok:
        print("? Local Live:  http://localhost:8000")
    else:
        print("?? Local Setup: Run 'start_system.bat' to start local server")
    
    print("\n?? QUICK START COMMANDS:")
    print("   start_system.bat        - Simple local system")
    print("   run_digital_twin.bat    - Advanced system") 
    print("   run_local.bat          - Development mode")
    
    if github_ok or local_ok:
        print("\n?? YOUR DIGITAL TWIN IS SUCCESSFULLY PUBLISHED!")
        
        # Ask if user wants to open demo
        try:
            choice = input("\n?? Open demo in browser? (y/n): ").lower().strip()
            if choice in ['y', 'yes', '']:
                open_demo()
        except KeyboardInterrupt:
            print("\n??  Demo not opened")
    
    else:
        print("\n??  Some issues detected. Check the logs above.")
    
    print(f"\n?? Test completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()