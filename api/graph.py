# -*- coding: utf-8 -*-
"""
LangGraph Cloud Integration for GHC Digital Twin System
Enhanced with real LangGraph deployment and API credentials
"""
from typing import TypedDict, List, Union, Dict, Any
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
import httpx
import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# State definition for LangGraph cloud integration
class AgentState(TypedDict):
    messages: List[BaseMessage]
    agent_type: str
    context: dict
    collaborating_agents: List[str]
    current_agent: str
    processed_by: List[str]
    final_response: str

# LangGraph Cloud Configuration - Using your real deployment!
DR_BASE_URL = os.getenv("DR_BASE_URL")
DR_API_KEY = os.getenv("DR_API_KEY")
LANGGRAPH_DEPLOYMENT_URL = os.getenv("LANGGRAPH_DEPLOYMENT_URL")

# Use the specific deployment URL if available
ACTIVE_DEPLOYMENT_URL = LANGGRAPH_DEPLOYMENT_URL or DR_BASE_URL

# Assistant IDs for different audiences
ASSISTANT_IDS = {
    "boardroom": os.getenv("ASSISTANT_ID_BOARDROOM"),
    "investor": os.getenv("ASSISTANT_ID_INVESTOR"), 
    "public": os.getenv("ASSISTANT_ID_PUBLIC"),
    "default": os.getenv("ASSISTANT_ID_PUBLIC")
}

print(f"?? LangGraph Deployment URL: {ACTIVE_DEPLOYMENT_URL}")
print(f"?? API Key configured: {'?' if DR_API_KEY else '?'}")
print(f"?? Using live deployment: {'?' if LANGGRAPH_DEPLOYMENT_URL else '?? fallback'}")

async def call_langgraph_deployment(question: str, agent_type: str = "ceo_digital_twin", audience: str = "public") -> Dict[str, Any]:
    """Call your live LangGraph deployment"""
    
    if not ACTIVE_DEPLOYMENT_URL or not DR_API_KEY:
        raise Exception("LangGraph deployment credentials not configured")
    
    headers = {
        "Authorization": f"Bearer {DR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # If using x-api-key format instead
    if DR_API_KEY.startswith("lsv2_"):
        headers = {
            "x-api-key": DR_API_KEY,
            "Content-Type": "application/json"
        }
    
    # Select appropriate assistant based on audience
    assistant_id = ASSISTANT_IDS.get(audience, ASSISTANT_IDS["default"])
    
    # Payload for your LangGraph deployment
    payload = {
        "input": {
            "question": question,
            "agent_type": agent_type,
            "audience": audience,
            "context": {
                "company": "Green Hill Canarias",
                "timestamp": datetime.now().isoformat(),
                "system_mode": "live"
            }
        },
        "config": {
            "configurable": {
                "thread_id": f"ghc_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"?? Calling LangGraph Deployment: {agent_type} for {audience}")
            print(f"?? URL: {ACTIVE_DEPLOYMENT_URL}")
            
            # Try different endpoints that might be available
            endpoints_to_try = [
                f"{ACTIVE_DEPLOYMENT_URL}/invoke",
                f"{ACTIVE_DEPLOYMENT_URL}/stream", 
                f"{ACTIVE_DEPLOYMENT_URL}/runs/wait",
                f"{ACTIVE_DEPLOYMENT_URL}"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = await client.post(
                        endpoint,
                        headers=headers,
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"? LangGraph deployment response received from {endpoint}")
                        return {
                            "success": True,
                            "response": result,
                            "source": "langgraph_deployment",
                            "agent_type": agent_type,
                            "endpoint": endpoint
                        }
                    else:
                        print(f"?? Endpoint {endpoint} returned {response.status_code}")
                        
                except Exception as e:
                    print(f"?? Failed endpoint {endpoint}: {e}")
                    continue
            
            # If no endpoint worked
            print("? All LangGraph endpoints failed - using fallback")
            return {"success": False, "error": "all_endpoints_failed", "fallback": True}
            
    except Exception as e:
        print(f"?? LangGraph deployment error: {e}")
        return {"success": False, "error": str(e), "fallback": True}

# Enhanced fallback responses with real company data
ENHANCED_RESPONSES = {
    "ceo_digital_twin": {
        "strategic": """As CEO Digital Twin of Green Hill Canarias, I'm pleased to report our strong Q3 2024 performance:

**Financial Highlights:**
- Revenue: 3.2M EUR (32% YoY growth)
- EBITDA Margin: 22% and improving
- Operating cash flow: Positive since Q2 2024

**Strategic Position:**
Our focus on precision agriculture and carbon-neutral operations positions us perfectly for market expansion across mainland Spain and North Africa. We're actively pursuing our Series A funding target of 8M EUR to accelerate technology infrastructure and operational scaling.

**Key Initiatives:**
- Technology integration across 750 hectares
- IoT sensor deployment and AI-driven analytics
- Supply chain optimization with 15 distribution partners

This sustainable agriculture leadership strategy creates significant competitive advantages in the growing ESG-focused market.""",
        
        "financial": """From a strategic financial perspective, Green Hill Canarias demonstrates exceptional fiscal health:

**Current Metrics:**
- Q3 2024 Revenue: 3.2M EUR (32% YoY growth)
- EBITDA Margin: 22% with operational efficiency gains
- Cash Flow: Positive trajectory since Q2 2024
- Funding Target: 8M EUR Series A for expansion

**Growth Drivers:**
- Precision agriculture technology adoption
- Market expansion into mainland Spain and North Africa
- ESG-focused sustainable practices attracting premium pricing
- Operational scaling across existing 750 hectares

**Investment Priorities:**
- Technology infrastructure enhancement
- Market expansion capabilities
- Talent acquisition (currently 180 employees including 45 engineers)
- Supply chain optimization

The sustainable agriculture market presents exceptional opportunities for accelerated growth.""",
        
        "operations": """Operationally, Green Hill Canarias demonstrates world-class performance across our agricultural operations:

**Operational Excellence:**
- 750 hectares across Gran Canaria and Tenerife
- 98.5% quality certification rate
- 12,000 tons annual production capacity
- 180-person team including 45 agricultural engineers and data scientists

**Technology Integration:**
- IoT sensors for real-time crop monitoring
- AI-driven analytics for yield optimization
- Smart irrigation systems (35% water usage reduction)
- Weather pattern analysis and predictive modeling

**Supply Chain:**
- 15 distribution partners across Spain
- Optimized logistics and delivery systems
- Quality control at every stage
- Traceability from farm to consumer

**Innovation Leadership:**
Our precision farming approach combines traditional agricultural knowledge with cutting-edge technology, resulting in 23% yield improvements while maintaining strict sustainability standards."""
    }
}

def generate_enhanced_response(agent_type: str, question: str, context: dict = None) -> str:
    """Generate enhanced fallback responses using real company knowledge"""
    
    # Determine response category based on question content
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["revenue", "financial", "money", "funding", "profit", "cost"]):
        category = "financial"
    elif any(word in question_lower for word in ["operation", "supply", "production", "efficiency", "hectares"]):
        category = "operations"
    else:
        category = "strategic"
    
    # Get base response
    agent_responses = ENHANCED_RESPONSES.get(agent_type, ENHANCED_RESPONSES["ceo_digital_twin"])
    base_response = agent_responses.get(category, agent_responses["strategic"])
    
    # Add question-specific context
    question_context = f"""
**Your Question:** "{question}"

**Analysis & Recommendations:**
Based on our current operational data and market position, this aligns with our strategic priorities for sustainable growth and market leadership in precision agriculture. I recommend data-driven analysis and stakeholder alignment for optimal outcomes.

**Next Steps:**
- Review detailed analytics and performance metrics
- Assess resource allocation and timeline requirements  
- Coordinate with relevant teams for implementation
- Monitor progress against established KPIs"""
    
    return base_response + question_context

# Agent processing functions with deployment integration
async def ceo_agent_node(state: AgentState) -> AgentState:
    """CEO Digital Twin with LangGraph deployment integration"""
    
    messages = state["messages"]
    agent_type = state.get("agent_type", "ceo_digital_twin")
    context = state.get("context", {})
    audience = context.get("audience", "public")
    
    # Get the last human message
    last_message = next((msg for msg in reversed(messages) if isinstance(msg, HumanMessage)), None)
    question = last_message.content if last_message else "Strategic analysis request"
    
    # Try LangGraph deployment first
    deployment_result = await call_langgraph_deployment(question, agent_type, audience)
    
    if deployment_result.get("success"):
        # Use real LangGraph deployment response
        deployment_response = deployment_result.get("response", {})
        
        # Extract response content (format may vary)
        if isinstance(deployment_response, dict):
            response_content = str(deployment_response.get("output", deployment_response.get("content", deployment_response)))
        else:
            response_content = str(deployment_response)
            
        processing_method = "langgraph_deployment"
        print("? Using LangGraph Deployment response")
    else:
        # Use enhanced fallback
        response_content = generate_enhanced_response(agent_type, question, context)
        processing_method = "enhanced_fallback"
        print("?? Using enhanced fallback response")
    
    # Update state
    ai_message = AIMessage(content=response_content)
    state["messages"].append(ai_message)
    state["current_agent"] = agent_type
    state["processed_by"].append(f"{agent_type}_{processing_method}")
    state["final_response"] = response_content
    
    return state

async def other_agent_node(state: AgentState) -> AgentState:
    """Handler for other agent types with deployment integration"""
    
    messages = state["messages"] 
    agent_type = state.get("agent_type", "ceo_digital_twin")
    context = state.get("context", {})
    audience = context.get("audience", "public")
    
    # Get the last human message
    last_message = next((msg for msg in reversed(messages) if isinstance(msg, HumanMessage)), None)
    question = last_message.content if last_message else "Analysis request"
    
    # Try LangGraph deployment first
    deployment_result = await call_langgraph_deployment(question, agent_type, audience)
    
    if deployment_result.get("success"):
        # Use real LangGraph deployment response
        deployment_response = deployment_result.get("response", {})
        
        if isinstance(deployment_response, dict):
            response_content = str(deployment_response.get("output", deployment_response.get("content", deployment_response)))
        else:
            response_content = str(deployment_response)
            
        processing_method = "langgraph_deployment"
        print(f"? Using LangGraph Deployment response for {agent_type}")
    else:
        # Use enhanced fallback
        response_content = generate_enhanced_response(agent_type, question, context)
        processing_method = "enhanced_fallback"
        print(f"?? Using enhanced fallback for {agent_type}")
    
    # Update state
    ai_message = AIMessage(content=response_content)
    state["messages"].append(ai_message)
    state["current_agent"] = agent_type
    state["processed_by"].append(f"{agent_type}_{processing_method}")
    state["final_response"] = response_content
    
    return state

def route_agent(state: AgentState) -> str:
    """Route to appropriate agent based on agent_type"""
    agent_type = state.get("agent_type", "ceo_digital_twin")
    
    if agent_type == "ceo_digital_twin":
        return "ceo_agent"
    else:
        return "other_agent"

def should_end(state: AgentState) -> bool:
    """Determine if processing should end"""
    return len(state.get("processed_by", [])) >= 1

# Build the enhanced LangGraph workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("ceo_agent", ceo_agent_node)
workflow.add_node("other_agent", other_agent_node)

# Add conditional routing from start
workflow.add_conditional_edges(
    START,
    route_agent,
    {
        "ceo_agent": "ceo_agent",
        "other_agent": "other_agent"
    }
)

# Add termination conditions
workflow.add_conditional_edges(
    "ceo_agent",
    lambda state: END if should_end(state) else "other_agent",
    {
        "other_agent": "other_agent",
        END: END
    }
)

workflow.add_conditional_edges(
    "other_agent",
    lambda state: END if should_end(state) else END,
    {END: END}
)

# Compile the graph
try:
    graph = workflow.compile()
    print("? Enhanced LangGraph with deployment integration compiled successfully")
    LANGGRAPH_COMPILED = True
except Exception as e:
    print(f"?? LangGraph compilation error: {e}")
    graph = None
    LANGGRAPH_COMPILED = False

# Export for use in the main application
__all__ = ["graph", "AgentState", "call_langgraph_deployment", "LANGGRAPH_COMPILED"]