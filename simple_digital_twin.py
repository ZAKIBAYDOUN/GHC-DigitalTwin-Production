"""
Simplified Digital Twin System for Local and Production Deployment
Green Hill Canarias - Startup Dashboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GHC Digital Twin System",
    description="Green Hill Canarias Digital Twin Dashboard",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AgentRequest(BaseModel):
    question: str
    agent_type: str = "ceo_digital_twin"
    audience: str = "public"
    language: str = "en"
    require_collaboration: bool = False

class ChatResponse(BaseModel):
    agent_type: str
    response: str
    confidence: float = 0.85
    knowledge_sources: List[str] = ["knowledge_base"]
    collaborating_agents: List[str] = []
    recommended_actions: List[str] = []
    metadata: Dict[str, Any] = {}
    timestamp: str = datetime.now().isoformat()

# Agent configurations
AGENT_CONFIG = {
    "ceo_digital_twin": {
        "name": "CEO Digital Twin",
        "specialization": ["strategic", "financial", "operations"],
        "personality": "As your Digital Twin CEO, I focus on strategic vision, growth opportunities, and high-level decision making."
    },
    "cfo_agent": {
        "name": "CFO Agent", 
        "specialization": ["financial", "compliance"],
        "personality": "From a financial perspective, I analyze numbers, projections, and investment opportunities."
    },
    "coo_agent": {
        "name": "COO Agent",
        "specialization": ["operations", "sustainability"],
        "personality": "I focus on operational efficiency, process optimization, and sustainable business practices."
    },
    "cmo_agent": {
        "name": "CMO Agent",
        "specialization": ["customer_data", "market_intelligence"],
        "personality": "I specialize in marketing strategy, customer insights, and growth initiatives."
    },
    "agricultural_intelligence": {
        "name": "Agricultural Intelligence Agent",
        "specialization": ["operations", "sustainability"],
        "personality": "I provide insights on crop management, sustainable farming, and agricultural optimization."
    },
    "sustainability_agent": {
        "name": "Sustainability Agent",
        "specialization": ["sustainability", "compliance"],
        "personality": "I focus on ESG metrics, environmental impact, and sustainable business practices."
    },
    "risk_management": {
        "name": "Risk Management Agent",
        "specialization": ["financial", "compliance", "operations"],
        "personality": "I assess risks, identify potential threats, and recommend mitigation strategies."
    },
    "compliance_agent": {
        "name": "Compliance Agent",
        "specialization": ["compliance", "financial"],
        "personality": "I ensure regulatory compliance and help navigate legal requirements."
    },
    "data_analytics": {
        "name": "Data Analytics Agent",
        "specialization": ["financial", "operations", "customer_data"],
        "personality": "I analyze data patterns, generate insights, and support data-driven decision making."
    },
    "customer_service": {
        "name": "Customer Service Agent",
        "specialization": ["customer_data", "operations"],
        "personality": "I focus on customer satisfaction, relationship management, and service optimization."
    }
}

# Mock knowledge base
KNOWLEDGE_BASE = {
    "strategic": [
        "Green Hill Canarias is a sustainable agriculture company focused on innovative farming practices.",
        "Our mission is to revolutionize agriculture through technology and sustainability.",
        "We target 25% growth annually through expansion and technology adoption."
    ],
    "financial": [
        "Current revenue run rate: $2.5M annually",
        "Profit margin: 18% and growing",
        "Investment needed: $5M for Series A expansion"
    ],
    "operations": [
        "Operating 500 hectares of sustainable farmland",
        "Employing 150+ agricultural specialists",
        "Implementing IoT sensors for crop monitoring"
    ],
    "sustainability": [
        "Carbon neutral operations by 2025",
        "Water usage reduced by 30% through smart irrigation",
        "Biodiversity increased by 40% through regenerative practices"
    ]
}

# Routes
@app.get("/")
async def root():
    """Serve the main dashboard"""
    if os.path.exists("index_digital_twin.html"):
        return FileResponse("index_digital_twin.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    else:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html><head><title>GHC Digital Twin</title></head>
        <body>
        <h1>?? Green Hill Canarias Digital Twin</h1>
        <p>System is running! API available at /api/</p>
        </body></html>
        """)

@app.get("/api/agents")
async def list_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {
                "type": agent_type,
                "name": config["name"],
                "specialization": config["specialization"]
            }
            for agent_type, config in AGENT_CONFIG.items()
        ]
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: AgentRequest):
    """Main chat endpoint"""
    try:
        agent_config = AGENT_CONFIG.get(request.agent_type, AGENT_CONFIG["ceo_digital_twin"])
        
        # Simulate knowledge retrieval
        relevant_knowledge = []
        for domain in agent_config["specialization"]:
            if domain in KNOWLEDGE_BASE:
                relevant_knowledge.extend(KNOWLEDGE_BASE[domain][:2])
        
        # Generate response
        context = " ".join(relevant_knowledge)
        response_text = f"{agent_config['personality']}\n\nBased on our knowledge: {context}\n\nRegarding your question: '{request.question}' - This requires strategic analysis and data-driven decision making. Let me provide you with actionable insights based on our current operations and market position."
        
        # Generate actions based on agent type
        action_map = {
            "ceo_digital_twin": ["Review strategic plan", "Analyze market opportunities", "Schedule leadership meeting"],
            "cfo_agent": ["Update financial projections", "Review budget allocations", "Assess investment opportunities"],
            "coo_agent": ["Optimize operations", "Review supply chain", "Implement efficiency measures"],
            "agricultural_intelligence": ["Monitor crop status", "Analyze weather patterns", "Optimize irrigation"],
        }
        
        actions = action_map.get(request.agent_type, ["Monitor developments", "Follow up on insights"])
        
        # Simulate collaboration if requested
        collaborators = []
        if request.require_collaboration:
            collab_map = {
                "ceo_digital_twin": ["cfo_agent", "coo_agent"],
                "cfo_agent": ["ceo_digital_twin", "risk_management"],
                "coo_agent": ["sustainability_agent", "agricultural_intelligence"]
            }
            collaborators = collab_map.get(request.agent_type, [])[:2]
        
        return ChatResponse(
            agent_type=request.agent_type,
            response=response_text,
            confidence=0.88,
            knowledge_sources=agent_config["specialization"],
            collaborating_agents=collaborators,
            recommended_actions=actions,
            metadata={
                "knowledge_items": len(relevant_knowledge),
                "domains_searched": agent_config["specialization"],
                "collaboration": request.require_collaboration
            }
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge/ingest")
async def ingest_knowledge(content: str, source: str, domain: str = "strategic"):
    """Simulate knowledge ingestion"""
    # In a real system, this would add to vector database
    logger.info(f"Would ingest: {source} to {domain}")
    return {"status": "success", "message": f"Added {source} to {domain} knowledge base"}

@app.get("/api/knowledge/stats")
async def knowledge_stats():
    """Get knowledge base statistics"""
    return {
        "domains": {
            domain: {
                "status": "available",
                "document_count": len(docs)
            }
            for domain, docs in KNOWLEDGE_BASE.items()
        },
        "last_updated": datetime.now().isoformat(),
        "total_domains": len(KNOWLEDGE_BASE)
    }

@app.get("/api/system/health")
async def system_health():
    """System health check"""
    return {
        "status": "healthy",
        "agents": len(AGENT_CONFIG),
        "knowledge_domains": len(KNOWLEDGE_BASE),
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("?? Starting Green Hill Canarias Digital Twin")
    print("?? 10 Specialized Agents Ready")
    print("?? Knowledge System Active")
    print("?? Server: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)