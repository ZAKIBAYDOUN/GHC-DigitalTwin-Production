import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

# Import fixed - tools module may not exist, making it optional
try:
    import tools
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False

# Cargar variables de entorno (root y local)
load_dotenv("../.env")
load_dotenv()
DR_BASE_URL = os.getenv("DR_BASE_URL", "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app")
DR_API_KEY = os.getenv("DR_API_KEY", "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")

# Make API keys optional for deployment
if not DR_BASE_URL or not DR_API_KEY:
    print("Warning: DR_BASE_URL or DR_API_KEY not configured. Using defaults.")

ASSISTANT_IDS = {
    "boardroom": "76f94782-5f1d-4ea0-8e69-294da3e1aefb",
    "investor": "ff7afd85-51e0-4fdd-8ec5-a14508a100f9",
    "public": "34747e20-39db-415e-bd80-597006f71a7a",
}

app = FastAPI(
    title="GHC Digital Twin API",
    description="Green Hill Canarias Digital Twin API Server",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskBody(BaseModel):
    audience: str
    question: str

@app.get("/api/health")
def health():
    return {"ok": True, "status": "healthy", "version": "1.0.0"}

@app.get("/api/system/health")
def system_health():
    """System health check for compatibility"""
    return {
        "status": "healthy",
        "agents": 10,
        "knowledge_domains": 4,
        "version": "1.0.0",
        "tools_available": TOOLS_AVAILABLE
    }

@app.get("/api/history")
def history():
    # Placeholder de historial
    return {"history": []}

@app.post("/api/ask")
def ask(body: AskBody):
    audience = body.audience.lower()
    if audience not in ASSISTANT_IDS:
        raise HTTPException(status_code=400, detail="Invalid audience")
    
    # If no API key configured, return mock response
    if not DR_API_KEY or DR_API_KEY == "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":
        return {
            "status": "mock_response",
            "response": f"Mock response for {audience} audience: {body.question}",
            "agent": audience
        }
    
    url = f"{DR_BASE_URL}/runs/wait"
    headers = {"x-api-key": DR_API_KEY, "Content-Type": "application/json"}
    payload = {
        "assistant_id": ASSISTANT_IDS[audience],
        "input": {"question": body.question},
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        error_detail = response.json() if response.content else str(http_err)
        raise HTTPException(status_code=response.status_code, detail=error_detail)
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {req_err}")

@app.post("/api/ingest")
def ingest():
    return {"status": "not_implemented"}

# --- Endpoints para Herramientas ---

@app.get("/api/tools")
def get_tools():
    """Devuelve la lista de definiciones de herramientas."""
    if TOOLS_AVAILABLE:
        return tools.get_tool_definitions()
    return {"tools": [], "message": "Tools module not available"}

class ToolExecutionBody(BaseModel):
    name: str
    args: dict

@app.post("/api/tools/execute")
def execute_tool_endpoint(body: ToolExecutionBody):
    """Ejecuta una herramienta y devuelve el resultado."""
    if not TOOLS_AVAILABLE:
        raise HTTPException(status_code=501, detail="Tools module not available")
    
    result = tools.execute_tool(body.name, body.args)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

# Add missing endpoints from simple_digital_twin.py for compatibility
@app.get("/api/agents")
def get_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {"type": "ceo_digital_twin", "name": "CEO Digital Twin", "specialization": ["strategic", "financial"]},
            {"type": "cfo_agent", "name": "CFO Agent", "specialization": ["financial", "compliance"]},
            {"type": "coo_agent", "name": "COO Agent", "specialization": ["operations", "sustainability"]},
            {"type": "cmo_agent", "name": "CMO Agent", "specialization": ["marketing", "customer_data"]},
            {"type": "agricultural_intelligence", "name": "Agricultural AI", "specialization": ["operations", "sustainability"]},
            {"type": "sustainability_agent", "name": "Sustainability Agent", "specialization": ["sustainability", "compliance"]},
            {"type": "risk_management", "name": "Risk Agent", "specialization": ["financial", "compliance"]},
            {"type": "compliance_agent", "name": "Compliance Agent", "specialization": ["compliance", "financial"]},
            {"type": "data_analytics", "name": "Analytics Agent", "specialization": ["financial", "operations"]},
            {"type": "customer_service", "name": "Customer Agent", "specialization": ["customer_data", "operations"]}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
