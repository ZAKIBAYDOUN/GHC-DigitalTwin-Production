#!/usr/bin/env python3
"""
GHC Digital Twin - Deployment Verification Script
Tests and validates all deployment configurations
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_file_exists(filepath, required=True):
    """Check if a file exists and return status"""
    exists = Path(filepath).exists()
    status = "?" if exists else ("?" if required else "??")
    print(f"{status} {filepath}")
    return exists

def validate_json_file(filepath):
    """Validate JSON file syntax"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"? {filepath} - Valid JSON")
        return True
    except Exception as e:
        print(f"? {filepath} - Invalid JSON: {e}")
        return False

def check_python_syntax(filepath):
    """Check Python file syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"? {filepath} - Valid Python syntax")
        return True
    except Exception as e:
        print(f"? {filepath} - Syntax error: {e}")
        return False

def main():
    print_header("GHC DIGITAL TWIN - DEPLOYMENT VALIDATION")
    
    os.chdir(Path(__file__).parent)
    
    # Core files check
    print_header("CORE FILES VALIDATION")
    
    core_files = [
        "index.html",
        "simple_digital_twin.py",
        "requirements.txt",
        "api/server.py",
        "api/requirements.txt",
        "api/graph.py",
        "langgraph.json",
        ".env.example",
        "README.md"
    ]
    
    all_core_exist = True
    for file in core_files:
        if not check_file_exists(file, required=True):
            all_core_exist = False
    
    # Deployment files check
    print_header("DEPLOYMENT FILES VALIDATION")
    
    deployment_files = [
        "Dockerfile",
        "docker-compose.yml",
        "frontend/Dockerfile", 
        "Procfile",
        "vercel.json",
        "netlify.toml",
        ".github/workflows/deploy.yml"
    ]
    
    for file in deployment_files:
        check_file_exists(file, required=False)
    
    # Scripts check
    print_header("STARTUP SCRIPTS VALIDATION")
    
    script_files = [
        "scripts/start_system.bat",
        "scripts/run_digital_twin.bat",
        "scripts/run_local.bat",
        "start_system.sh"
    ]
    
    for file in script_files:
        check_file_exists(file, required=False)
    
    # JSON files validation
    print_header("JSON CONFIGURATION VALIDATION")
    
    json_files = ["langgraph.json", "vercel.json", "frontend/package.json"]
    for file in json_files:
        if Path(file).exists():
            validate_json_file(file)
    
    # Python syntax validation
    print_header("PYTHON SYNTAX VALIDATION")
    
    python_files = [
        "simple_digital_twin.py",
        "api/server.py", 
        "api/graph.py",
        "api/tools.py"
    ]
    
    for file in python_files:
        if Path(file).exists():
            check_python_syntax(file)
    
    # Requirements analysis
    print_header("REQUIREMENTS ANALYSIS")
    
    if Path("requirements.txt").exists():
        with open("requirements.txt") as f:
            root_reqs = f.read().strip().split('\n')
        print(f"? Root requirements.txt: {len(root_reqs)} packages")
    
    if Path("api/requirements.txt").exists():
        with open("api/requirements.txt") as f:
            api_reqs = f.read().strip().split('\n')
        print(f"? API requirements.txt: {len(api_reqs)} packages")
    
    # Environment configuration
    print_header("ENVIRONMENT CONFIGURATION")
    
    if check_file_exists(".env.example", required=False):
        print("?? Environment template available")
        
    if check_file_exists(".env", required=False):
        print("?? Environment file configured")
    else:
        print("?? .env file not found (will be created on first run)")
    
    # Git configuration
    print_header("GIT & DEPLOYMENT READINESS")
    
    if Path(".git").exists():
        print("? Git repository initialized")
        
        # Check for GitHub Pages deployment
        if Path(".github/workflows/deploy.yml").exists():
            print("? GitHub Actions workflow configured")
        
        try:
            result = subprocess.run(["git", "remote", "-v"], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and "github.com" in result.stdout:
                print("? GitHub remote configured")
            else:
                print("?? GitHub remote not configured")
        except:
            print("?? Could not check Git remotes")
    else:
        print("?? Not a Git repository")
    
    # Final summary
    print_header("DEPLOYMENT SUMMARY")
    
    if all_core_exist:
        print("? CORE FILES: All essential files present")
    else:
        print("? CORE FILES: Missing essential files")
    
    print("\n?? DEPLOYMENT OPTIONS AVAILABLE:")
    print("   1. Local Development: scripts/start_system.bat or ./start_system.sh")
    print("   2. Docker: docker-compose up")
    print("   3. Heroku: git push heroku main (with Procfile)")
    print("   4. Vercel: vercel deploy (with vercel.json)")
    print("   5. Netlify: netlify deploy (with netlify.toml)")
    print("   6. GitHub Pages: Push to main branch (automatic)")
    
    print("\n?? QUICK START:")
    print("   Windows: scripts\\start_system.bat")
    print("   Linux/Mac: ./start_system.sh")
    print("   Docker: docker-compose up --build")
    
    if all_core_exist:
        print("\n?? YOUR GIT APP IS READY FOR DEPLOYMENT!")
        return True
    else:
        print("\n?? Please fix missing files before deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)