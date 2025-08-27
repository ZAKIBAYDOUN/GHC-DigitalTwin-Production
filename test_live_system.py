# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
GHC Digital Twin Live System Test Suite
Comprehensive testing of all AI agents and system capabilities
"""
import asyncio
import httpx
import json
import time
from datetime import datetime
import sys

class DigitalTwinTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_system_health(self):
        """Test basic system health and status"""
        print("?? Testing System Health...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/system/health", timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"? System Status: {data.get('status')}")
                    print(f"? System Mode: {data.get('system_mode')}")
                    print(f"? Agents Available: {data.get('agents')}")
                    print(f"? Knowledge Domains: {data.get('knowledge_domains')}")
                    
                    capabilities = data.get('capabilities', {})
                    print(f"?? LangGraph Enabled: {capabilities.get('langgraph_enabled')}")
                    print(f"?? External API Enabled: {capabilities.get('external_api_enabled')}")
                    print(f"?? Enhanced Knowledge: {capabilities.get('enhanced_knowledge')}")
                    
                    self.test_results.append(("System Health", "PASS", data.get('status')))
                    return True
                else:
                    print(f"? Health check failed with status: {response.status_code}")
                    self.test_results.append(("System Health", "FAIL", f"HTTP {response.status_code}"))
                    return False
                    
        except Exception as e:
            print(f"? Health check error: {e}")
            self.test_results.append(("System Health", "ERROR", str(e)))
            return False
    
    async def test_agent_listing(self):
        """Test agent listing endpoint"""
        print("\n?? Testing Agent Listing...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/agents", timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    agents = data.get('agents', [])
                    total_agents = data.get('total_agents', 0)
                    
                    print(f"? Total Agents: {total_agents}")
                    print(f"? LangGraph Integration: {data.get('langgraph_enabled')}")
                    
                    for agent in agents[:5]:  # Show first 5 agents
                        print(f"  • {agent.get('name')} ({agent.get('type')})")
                        print(f"    Specializations: {', '.join(agent.get('specialization', []))}")
                        print(f"    Capabilities: {len(agent.get('capabilities', []))} skills")
                    
                    if len(agents) > 5:
                        print(f"  ... and {len(agents) - 5} more agents")
                    
                    self.test_results.append(("Agent Listing", "PASS", f"{total_agents} agents"))
                    return True
                else:
                    print(f"? Agent listing failed: {response.status_code}")
                    self.test_results.append(("Agent Listing", "FAIL", f"HTTP {response.status_code}"))
                    return False
                    
        except Exception as e:
            print(f"? Agent listing error: {e}")
            self.test_results.append(("Agent Listing", "ERROR", str(e)))
            return False
    
    async def test_agent_chat(self, agent_type, question, test_name):
        """Test individual agent chat functionality"""
        print(f"\n?? Testing {test_name}...")
        
        chat_request = {
            "question": question,
            "agent_type": agent_type,
            "require_collaboration": False,
            "audience": "public"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=chat_request,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"? Agent Type: {result.get('agent_type')}")
                    print(f"? System Mode: {result.get('system_mode')}")
                    print(f"?? Confidence: {result.get('confidence')}")
                    print(f"?? Knowledge Sources: {', '.join(result.get('knowledge_sources', []))}")
                    print(f"?? Processing Method: {result.get('metadata', {}).get('processing_method', 'standard')}")
                    
                    response_text = result.get('response', '')
                    if len(response_text) > 150:
                        print(f"?? Response: {response_text[:150]}...")
                    else:
                        print(f"?? Response: {response_text}")
                    
                    actions = result.get('recommended_actions', [])
                    if actions:
                        print(f"?? Actions: {', '.join(actions[:3])}")
                    
                    collaborators = result.get('collaborating_agents', [])
                    if collaborators:
                        print(f"?? Collaborators: {', '.join(collaborators)}")
                    
                    self.test_results.append((test_name, "PASS", f"Confidence: {result.get('confidence')}"))
                    return True
                else:
                    print(f"? Chat failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"Error: {error_data}")
                    except:
                        pass
                    self.test_results.append((test_name, "FAIL", f"HTTP {response.status_code}"))
                    return False
                    
        except Exception as e:
            print(f"? Chat error: {e}")
            self.test_results.append((test_name, "ERROR", str(e)))
            return False

    async def run_comprehensive_tests(self):
        """Run all system tests"""
        print("?? GHC DIGITAL TWIN SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"?? Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"?? Testing System: {self.base_url}")
        print()
        
        # Test 1: System Health
        health_ok = await self.test_system_health()
        
        if not health_ok:
            print("\n? System health check failed. Please ensure the server is running.")
            return False
        
        # Test 2: Agent Listing
        await self.test_agent_listing()
        
        # Test 3: Individual Agent Tests
        agent_tests = [
            ("ceo_digital_twin", "What is our current strategic position and growth outlook?", "CEO Digital Twin"),
            ("cfo_agent", "Analyze our financial performance and funding requirements", "CFO Agent"),
            ("agricultural_intelligence", "How are our crops performing this season?", "Agricultural Intelligence"),
            ("sustainability_agent", "What's our progress on carbon neutrality goals?", "Sustainability Agent")
        ]
        
        for agent_type, question, test_name in agent_tests:
            await self.test_agent_chat(agent_type, question, test_name)
            await asyncio.sleep(1)  # Brief pause between tests
        
        # Test Summary
        self.print_test_summary()
        
        return True
    
    def print_test_summary(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("?? TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r[1] == "PASS"])
        failed_tests = len([r for r in self.test_results if r[1] == "FAIL"])
        error_tests = len([r for r in self.test_results if r[1] == "ERROR"])
        
        print(f"?? Total Tests: {total_tests}")
        print(f"? Passed: {passed_tests}")
        print(f"? Failed: {failed_tests}")
        print(f"?? Errors: {error_tests}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"?? Success Rate: {success_rate:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, status, details in self.test_results:
            status_icon = {"PASS": "?", "FAIL": "?", "ERROR": "??"}.get(status, "?")
            print(f"  {status_icon} {test_name}: {status} - {details}")
        
        print(f"\n?? Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success_rate >= 80:
            print("\n?? SYSTEM STATUS: READY FOR PRODUCTION!")
        elif success_rate >= 60:
            print("\n?? SYSTEM STATUS: MOSTLY FUNCTIONAL - Minor issues detected")
        else:
            print("\n? SYSTEM STATUS: NEEDS ATTENTION - Multiple failures detected")

async def main():
    """Main test execution"""
    tester = DigitalTwinTester()
    
    try:
        await tester.run_comprehensive_tests()
    except KeyboardInterrupt:
        print("\n?? Tests interrupted by user")
    except Exception as e:
        print(f"\n?? Unexpected error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("?? Starting GHC Digital Twin Live System Tests...")
    asyncio.run(main())