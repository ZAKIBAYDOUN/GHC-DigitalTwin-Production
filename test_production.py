#!/usr/bin/env python3
"""
GHC Digital Twin Live System - Production Test Suite
Test your real LangGraph integration
"""
import asyncio
import httpx
import json
import time
from datetime import datetime

async def test_live_system():
    """Test the live system with real LangGraph integration"""
    base_url = "http://localhost:8000"
    
    print("?? GHC DIGITAL TWIN LIVE SYSTEM TEST")
    print("=" * 50)
    print(f"?? {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"?? Testing: {base_url}")
    print()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: System Health
        print("1. ?? Testing System Health...")
        try:
            response = await client.get(f"{base_url}/api/system/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ? Status: {data.get('status')}")
                print(f"   ?? Agents: {data.get('agents')}")
                print(f"   ?? LangGraph: {data.get('capabilities', {}).get('langgraph_enabled')}")
                print(f"   ?? External API: {data.get('capabilities', {}).get('external_api_enabled')}")
                print(f"   ?? Knowledge: {data.get('knowledge_domains')} domains")
            else:
                print(f"   ? Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ? Connection error: {e}")
            return False
        
        # Test 2: Agent List
        print("\n2. ?? Testing Agent Availability...")
        try:
            response = await client.get(f"{base_url}/api/agents")
            if response.status_code == 200:
                data = response.json()
                agents = data.get('agents', [])
                print(f"   ? {len(agents)} agents available")
                print(f"   ?? LangGraph enabled: {data.get('langgraph_enabled')}")
                
                # Show some agents
                for agent in agents[:3]:
                    print(f"      • {agent.get('name')} - {len(agent.get('capabilities', []))} skills")
            else:
                print(f"   ? Agent list failed: {response.status_code}")
        except Exception as e:
            print(f"   ? Agent list error: {e}")
        
        # Test 3: CEO Digital Twin (Real LangGraph)
        print("\n3. ?? Testing CEO Digital Twin with LangGraph...")
        try:
            test_question = "What is our current strategic position and revenue outlook for Green Hill Canarias?"
            
            chat_request = {
                "question": test_question,
                "agent_type": "ceo_digital_twin",
                "audience": "boardroom",
                "require_collaboration": False
            }
            
            print(f"   ?? Question: {test_question}")
            print("   ?? Processing with LangGraph cloud...")
            
            response = await client.post(
                f"{base_url}/api/chat",
                json=chat_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ? Response received!")
                print(f"   ?? Agent: {result.get('agent_type')}")
                print(f"   ?? Confidence: {result.get('confidence')}")
                print(f"   ?? Processing: {result.get('metadata', {}).get('processing_method', 'unknown')}")
                
                response_text = result.get('response', '')
                if len(response_text) > 200:
                    print(f"   ?? Response: {response_text[:200]}...")
                else:
                    print(f"   ?? Response: {response_text}")
                    
                actions = result.get('recommended_actions', [])
                if actions:
                    print(f"   ?? Actions: {', '.join(actions[:2])}")
                    
            else:
                print(f"   ? CEO chat failed: {response.status_code}")
                error = response.text
                print(f"   Error: {error[:100]}...")
                
        except Exception as e:
            print(f"   ? CEO test error: {e}")
        
        # Test 4: Agricultural Intelligence
        print("\n4. ?? Testing Agricultural Intelligence...")
        try:
            chat_request = {
                "question": "How are our crops performing this season across our 750 hectares?",
                "agent_type": "agricultural_intelligence",
                "audience": "public",
                "require_collaboration": False
            }
            
            response = await client.post(
                f"{base_url}/api/chat",
                json=chat_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ? Agricultural AI responded!")
                print(f"   ?? Confidence: {result.get('confidence')}")
                response_text = result.get('response', '')[:150]
                print(f"   ?? Insight: {response_text}...")
            else:
                print(f"   ? Agricultural test failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ? Agricultural test error: {e}")
        
        # Test 5: System Status
        print("\n5. ?? Testing System Status...")
        try:
            response = await client.get(f"{base_url}/api/system/status")
            if response.status_code == 200:
                data = response.json()
                print(f"   ? System mode: {data.get('mode')}")
                features = data.get('features', {})
                print(f"   ?? LangGraph: {features.get('langgraph', {}).get('enabled')}")
                print(f"   ?? External API: {features.get('external_api', {}).get('enabled')}")
                print(f"   ?? Enhanced Knowledge: {features.get('enhanced_knowledge', {}).get('enabled')}")
            else:
                print(f"   ? Status check failed: {response.status_code}")
        except Exception as e:
            print(f"   ? Status error: {e}")
    
    print("\n" + "=" * 50)
    print("?? GHC DIGITAL TWIN LIVE SYSTEM TEST COMPLETE")
    print("=" * 50)
    print("?? Dashboard: http://localhost:8000")
    print("?? API Documentation: http://localhost:8000/docs")
    print("?? Real AI agents with LangGraph cloud integration")
    print("?? Using your production credentials")
    print("?? Ready for executive decision support!")
    return True

async def main():
    try:
        await test_live_system()
    except KeyboardInterrupt:
        print("\n?? Test interrupted")
    except Exception as e:
        print(f"\n?? Test error: {e}")

if __name__ == "__main__":
    asyncio.run(main())