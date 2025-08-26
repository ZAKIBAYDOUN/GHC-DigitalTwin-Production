#!/usr/bin/env python3
"""
Test script for GHC Digital Twin local development setup
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"? {method} {endpoint} - OK")
            return True, response.json()
        else:
            print(f"? {method} {endpoint} - Status: {response.status_code}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"? {method} {endpoint} - Connection failed (server not running?)")
        return False, None
    except Exception as e:
        print(f"? {method} {endpoint} - Error: {e}")
        return False, None

def main():
    print("?? Testing GHC Digital Twin Local Server")
    print("=" * 45)
    
    # Test health endpoint
    success, health_data = test_endpoint("/health")
    if success and health_data:
        print(f"   Mode: {health_data.get('mode')}")
        print(f"   Agent Available: {health_data.get('digital_roots_available')}")
    
    # Test config endpoint
    success, config_data = test_endpoint("/config")
    if success and config_data:
        print(f"   Current Mode: {config_data.get('mode')}")
    
    # Test chat endpoint with different audiences
    test_questions = [
        {"question": "What is Green Hill Canarias?", "audience": "public"},
        {"question": "What are the financial projections?", "audience": "investor"},
        {"question": "What are our strategic priorities?", "audience": "boardroom"}
    ]
    
    for test_case in test_questions:
        success, response = test_endpoint("/chat", "POST", test_case)
        if success:
            audience = test_case['audience']
            response_length = len(response.get('response', ''))
            print(f"   {audience.capitalize()} chat: {response_length} chars")
    
    print("\n?? Integration Test")
    print("-" * 20)
    
    # Full integration test
    try:
        # Get health
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"? Server running in {health_data['mode']} mode")
            
            # Test chat
            chat_data = {
                "question": "Hello, can you introduce yourself?",
                "audience": "public",
                "language": "en"
            }
            
            start_time = time.time()
            chat_response = requests.post(f"{BASE_URL}/chat", json=chat_data, timeout=15)
            response_time = (time.time() - start_time) * 1000
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                print(f"? Chat response received ({response_time:.0f}ms)")
                print(f"   Response preview: {result['response'][:100]}...")
                
                if result['metadata']['mode'] == 'local':
                    print("?? Using local digital-roots agent")
                else:
                    print("?? Using remote DigitalRoots API")
                
            else:
                print(f"? Chat failed: {chat_response.status_code}")
        
        else:
            print(f"? Health check failed: {health_response.status_code}")
    
    except Exception as e:
        print(f"? Integration test failed: {e}")
    
    print("\n" + "=" * 45)
    print("?? Test Complete")
    
    print("\n?? Next Steps:")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Select an audience and test the chat interface")
    print("3. Try switching between local and remote modes")
    print("4. Check the debug panel for detailed information")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        print("? Waiting 5 seconds for server to start...")
        time.sleep(5)
    
    main()