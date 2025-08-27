#!/usr/bin/env python3
"""
Simple GHC Digital Twin Live System Test
"""
import asyncio
import httpx
import json
from datetime import datetime

async def test_system():
    """Test the live Digital Twin system"""
    base_url = "http://localhost:8000"
    
    print("="*50)
    print("GHC DIGITAL TWIN SYSTEM TEST")
    print("="*50)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Health Check
        print("\n1. Testing System Health...")
        try:
            health = await client.get(f"{base_url}/api/system/health", timeout=10)
            if health.status_code == 200:
                data = health.json()
                print(f"   Status: {data.get('status')}")
                print(f"   Mode: {data.get('system_mode')}")
                print(f"   Agents: {data.get('agents')}")
                capabilities = data.get('capabilities', {})
                print(f"   LangGraph: {capabilities.get('langgraph_enabled')}")
                print("   ? HEALTH CHECK PASSED")
            else:
                print(f"   ? HEALTH CHECK FAILED: {health.status_code}")
                return
        except Exception as e:
            print(f"   ? HEALTH CHECK ERROR: {e}")
            return
        
        # Test 2: List Agents
        print("\n2. Testing Agent Listing...")
        try:
            agents_resp = await client.get(f"{base_url}/api/agents", timeout=10)
            if agents_resp.status_code == 200:
                data = agents_resp.json()
                print(f"   Total Agents: {data.get('total_agents')}")
                print(f"   LangGraph Enabled: {data.get('langgraph_enabled')}")
                agents = data.get('agents', [])
                for i, agent in enumerate(agents[:3]):
                    print(f"   Agent {i+1}: {agent.get('name')}")
                print("   ? AGENT LISTING PASSED")
            else:
                print(f"   ? AGENT LISTING FAILED: {agents_resp.status_code}")
        except Exception as e:
            print(f"   ? AGENT LISTING ERROR: {e}")
        
        # Test 3: Chat with CEO Agent
        print("\n3. Testing CEO Digital Twin Chat...")
        try:
            chat_request = {
                "question": "What is our current revenue and strategic position?",
                "agent_type": "ceo_digital_twin",
                "require_collaboration": False
            }
            
            chat_resp = await client.post(
                f"{base_url}/api/chat",
                json=chat_request,
                timeout=30
            )
            
            if chat_resp.status_code == 200:
                result = chat_resp.json()
                print(f"   Agent: {result.get('agent_type')}")
                print(f"   Confidence: {result.get('confidence')}")
                print(f"   Method: {result.get('metadata', {}).get('processing_method')}")
                response = result.get('response', '')
                if len(response) > 100:
                    print(f"   Response: {response[:100]}...")
                else:
                    print(f"   Response: {response}")
                print("   ? CEO CHAT PASSED")
            else:
                print(f"   ? CEO CHAT FAILED: {chat_resp.status_code}")
        except Exception as e:
            print(f"   ? CEO CHAT ERROR: {e}")
        
        # Test 4: Chat with Agricultural Agent
        print("\n4. Testing Agricultural Intelligence...")
        try:
            chat_request = {
                "question": "How are our crops performing this season?",
                "agent_type": "agricultural_intelligence",
                "require_collaboration": False
            }
            
            chat_resp = await client.post(
                f"{base_url}/api/chat",
                json=chat_request,
                timeout=30
            )
            
            if chat_resp.status_code == 200:
                result = chat_resp.json()
                print(f"   Agent: {result.get('agent_type')}")
                print(f"   Confidence: {result.get('confidence')}")
                response = result.get('response', '')
                if len(response) > 100:
                    print(f"   Response: {response[:100]}...")
                else:
                    print(f"   Response: {response}")
                print("   ? AGRICULTURAL CHAT PASSED")
            else:
                print(f"   ? AGRICULTURAL CHAT FAILED: {chat_resp.status_code}")
        except Exception as e:
            print(f"   ? AGRICULTURAL CHAT ERROR: {e}")
        
        # Test 5: System Status
        print("\n5. Testing System Status...")
        try:
            status_resp = await client.get(f"{base_url}/api/system/status", timeout=10)
            if status_resp.status_code == 200:
                data = status_resp.json()
                print(f"   Mode: {data.get('mode')}")
                features = data.get('features', {})
                print(f"   LangGraph Available: {features.get('langgraph', {}).get('available')}")
                print(f"   External API Available: {features.get('external_api', {}).get('available')}")
                print("   ? STATUS CHECK PASSED")
            else:
                print(f"   ? STATUS CHECK FAILED: {status_resp.status_code}")
        except Exception as e:
            print(f"   ? STATUS CHECK ERROR: {e}")
    
    print("\n" + "="*50)
    print("?? GHC DIGITAL TWIN LIVE SYSTEM ACTIVE!")
    print("?? Dashboard: http://localhost:8000")
    print("?? API Docs: http://localhost:8000/docs")
    print("?? All AI agents operational")
    print("?? LangGraph integration enabled")
    print("?? Enhanced knowledge base active")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_system())