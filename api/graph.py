"""
LangGraph graph definition for GHC Digital Twin System
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel
import json

class AgentState(BaseModel):
    messages: list[BaseMessage] = []
    agent_type: str = "ceo_digital_twin"
    context: Dict[str, Any] = {}
    current_step: str = "start"

def routing_node(state: AgentState) -> Dict[str, Any]:
    """Route to appropriate agent based on request"""
    return {"current_step": "process"}

def ceo_agent_node(state: AgentState) -> Dict[str, Any]:
    """CEO Digital Twin Agent"""
    last_message = state.messages[-1] if state.messages else HumanMessage(content="Hello")
    
    response = AIMessage(content=f"""
    As your CEO Digital Twin, I analyze this from a strategic perspective.
    
    Based on your query: {last_message.content}
    
    Strategic Insights:
    - Market position: Strong growth trajectory in sustainable agriculture
    - Key priorities: Technology integration, sustainability metrics, expansion
    - Risk factors: Market volatility, regulatory changes
    - Opportunities: ESG investments, precision agriculture, carbon credits
    
    Recommended actions:
    1. Review quarterly performance metrics
    2. Assess market expansion opportunities  
    3. Strengthen sustainability initiatives
    """)
    
    return {
        "messages": state.messages + [response],
        "current_step": "complete"
    }

def other_agent_node(state: AgentState) -> Dict[str, Any]:
    """Generic agent handler for other agent types"""
    last_message = state.messages[-1] if state.messages else HumanMessage(content="Hello")
    
    agent_responses = {
        "cfo_agent": "From a financial perspective, our metrics show strong performance with 18% margins and growing revenue.",
        "coo_agent": "Operationally, we're optimizing efficiency across 500 hectares with IoT-enabled monitoring systems.",
        "agricultural_intelligence": "Crop data indicates optimal growing conditions with 23% improved yield through precision agriculture.",
        "sustainability_agent": "ESG metrics show we're on track for carbon neutrality by 2025 with 30% water usage reduction."
    }
    
    response_text = agent_responses.get(
        state.agent_type, 
        f"As the {state.agent_type}, I'm analyzing your request for strategic insights."
    )
    
    response = AIMessage(content=f"{response_text}\n\nRegarding: {last_message.content}")
    
    return {
        "messages": state.messages + [response],
        "current_step": "complete"
    }

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("routing", routing_node)
workflow.add_node("ceo_agent", ceo_agent_node)
workflow.add_node("other_agent", other_agent_node)

# Add edges
workflow.set_entry_point("routing")
workflow.add_conditional_edges(
    "routing",
    lambda state: "ceo_agent" if state.agent_type == "ceo_digital_twin" else "other_agent",
    {
        "ceo_agent": "ceo_agent",
        "other_agent": "other_agent"
    }
)

workflow.add_edge("ceo_agent", END)
workflow.add_edge("other_agent", END)

# Compile the graph
graph = workflow.compile()

# Export for langgraph.json
__all__ = ["graph"]