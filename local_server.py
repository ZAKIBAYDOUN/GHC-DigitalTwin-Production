"""
Local development server for GHC Digital Twin
Bridges the frontend with digital-roots agent locally
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import httpx
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add digital-roots to Python path
DIGITAL_ROOTS_PATH = os.getenv('DIGITAL_ROOTS_PATH', r"C:\Users\zakib\source\repos\ZAKIBAYDOUN\digital-roots")
if os.path.exists(DIGITAL_ROOTS_PATH):
    sys.path.insert(0, DIGITAL_ROOTS_PATH)
    logger.info(f"Added digital-roots path: {DIGITAL_ROOTS_PATH}")

app = FastAPI(
    title="GHC Digital Twin Local Server",
    description="Local development server for GHC Digital Twin",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    question: str
    audience: str = "public"
    language: str = "en"
    assistant_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    audience: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    mode: str
    digital_roots_path: str
    digital_roots_available: bool
    timestamp: datetime
    version: str

# Configuration
LOCAL_CONFIG = {
    "USE_LOCAL_AGENT": os.getenv('USE_LOCAL_AGENT', 'true').lower() == 'true',
    "DIGITAL_ROOTS_API": os.getenv('DR_BASE_URL', "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app"),
    "API_KEY": os.getenv('DR_API_KEY', "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"),
    "ASSISTANT_IDS": {
        "boardroom": os.getenv('ASSISTANT_ID_BOARDROOM', "76f94782-5f1d-4ea0-8e69-294da3e1aefb"),
        "investor": os.getenv('ASSISTANT_ID_INVESTOR', "ff7afd85-51e0-4fdd-8ec5-a14508a100f9"),
        "public": os.getenv('ASSISTANT_ID_PUBLIC', "34747e20-39db-415e-bd80-597006f71a7a")
    },
    "DEBUG_MODE": os.getenv('DEBUG_MODE', 'true').lower() == 'true',
    "HOST": os.getenv('LOCAL_SERVER_HOST', '0.0.0.0'),
    "PORT": int(os.getenv('LOCAL_SERVER_PORT', '8000'))
}

# Try to import local agent
local_agent = None
local_agent_available = False

try:
    # Try different possible import paths for your agent
    import_attempts = [
        "agent.main.DigitalRootsAgent",
        "main.DigitalRootsAgent", 
        "digital_roots_agent.DigitalRootsAgent",
        "src.agent.DigitalRootsAgent"
    ]
    
    for import_path in import_attempts:
        try:
            parts = import_path.split('.')
            module_name = '.'.join(parts[:-1])
            class_name = parts[-1]
            
            module = __import__(module_name, fromlist=[class_name])
            agent_class = getattr(module, class_name)
            local_agent = agent_class()
            local_agent_available = True
            
            logger.info(f"? Local digital-roots agent loaded from {import_path}")
            break
            
        except (ImportError, AttributeError) as e:
            continue
    
    if not local_agent_available:
        logger.warning("?? Could not import local agent with any standard paths")
        LOCAL_CONFIG["USE_LOCAL_AGENT"] = False

except Exception as e:
    logger.error(f"? Error loading local agent: {e}")
    LOCAL_CONFIG["USE_LOCAL_AGENT"] = False
    local_agent_available = False

# Create static directory if it doesn't exist
Path("static").mkdir(exist_ok=True)

@app.get("/")
async def read_index():
    """Serve the main index.html"""
    if os.path.exists("index_local.html"):
        return FileResponse('index_local.html')
    elif os.path.exists("index.html"):
        return FileResponse('index.html')
    else:
        return {"message": "Welcome to GHC Digital Twin Local Server", "endpoints": ["/health", "/config", "/chat"]}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        mode="local" if LOCAL_CONFIG["USE_LOCAL_AGENT"] and local_agent_available else "remote",
        digital_roots_path=DIGITAL_ROOTS_PATH,
        digital_roots_available=local_agent_available,
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "mode": "local" if LOCAL_CONFIG["USE_LOCAL_AGENT"] and local_agent_available else "remote",
        "assistant_ids": LOCAL_CONFIG["ASSISTANT_IDS"],
        "api_endpoint": f"http://localhost:{LOCAL_CONFIG['PORT']}" if LOCAL_CONFIG["USE_LOCAL_AGENT"] else LOCAL_CONFIG["DIGITAL_ROOTS_API"],
        "digital_roots_available": local_agent_available,
        "debug_mode": LOCAL_CONFIG["DEBUG_MODE"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - routes to local agent or remote API"""
    try:
        if LOCAL_CONFIG["USE_LOCAL_AGENT"] and local_agent_available:
            # Use local agent
            logger.info(f"?? Processing locally for {request.audience} audience")
            response = await process_with_local_agent(request)
            
        else:
            # Use remote API
            logger.info(f"?? Processing via remote API for {request.audience} audience")
            response = await process_with_remote_api(request)
        
        return ChatResponse(
            response=response,
            audience=request.audience,
            timestamp=datetime.now(),
            metadata={
                "mode": "local" if LOCAL_CONFIG["USE_LOCAL_AGENT"] and local_agent_available else "remote",
                "language": request.language,
                "agent_available": local_agent_available
            }
        )
        
    except Exception as e:
        logger.error(f"? Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_with_local_agent(request: ChatRequest) -> str:
    """Process request with local digital-roots agent"""
    try:
        # This is a flexible implementation that tries different agent interfaces
        
        # Method 1: Try async process method
        if hasattr(local_agent, 'aprocess'):
            result = await local_agent.aprocess(
                question=request.question,
                audience=request.audience,
                language=request.language
            )
            if isinstance(result, dict):
                return result.get('response', str(result))
            return str(result)
        
        # Method 2: Try sync process method
        elif hasattr(local_agent, 'process'):
            result = local_agent.process(
                question=request.question,
                audience=request.audience,
                language=request.language
            )
            if isinstance(result, dict):
                return result.get('response', str(result))
            return str(result)
        
        # Method 3: Try direct call
        elif callable(local_agent):
            result = local_agent(request.question, request.audience)
            return str(result)
        
        # Method 4: Try common method names
        for method_name in ['run', 'execute', 'chat', 'ask']:
            if hasattr(local_agent, method_name):
                method = getattr(local_agent, method_name)
                result = method(request.question)
                return str(result)
        
        # Fallback: Mock response for development
        return f"[LOCAL AGENT] Mock response for {request.audience}: {request.question[:50]}..."
            
    except Exception as e:
        logger.error(f"Error with local agent: {e}")
        logger.info("Falling back to remote API")
        return await process_with_remote_api(request)

async def process_with_remote_api(request: ChatRequest) -> str:
    """Process request with remote DigitalRoots API"""
    async with httpx.AsyncClient() as client:
        try:
            assistant_id = request.assistant_id or LOCAL_CONFIG["ASSISTANT_IDS"].get(
                request.audience, 
                LOCAL_CONFIG["ASSISTANT_IDS"]["public"]
            )
            
            payload = {
                "assistant_id": assistant_id,
                "input": {
                    "question": request.question,
                    "audience": request.audience,
                    "language": request.language
                }
            }
            
            logger.debug(f"Sending to remote API: {payload}")
            
            response = await client.post(
                f"{LOCAL_CONFIG['DIGITAL_ROOTS_API']}/runs/wait",
                headers={
                    "x-api-key": LOCAL_CONFIG["API_KEY"],
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API returned status {response.status_code}: {response.text}")
            
            data = response.json()
            logger.debug(f"Remote API response: {data}")
            
            # Extract response from API data structure
            if data.get('output') and data['output'].get('response'):
                return data['output']['response']
            elif data.get('response'):
                return data['response']
            else:
                return str(data)
                
        except Exception as e:
            raise Exception(f"Remote API error: {str(e)}")

@app.post("/toggle-mode")
async def toggle_mode():
    """Toggle between local and remote mode"""
    if not local_agent_available:
        return {"error": "Local agent not available", "mode": "remote"}
    
    LOCAL_CONFIG["USE_LOCAL_AGENT"] = not LOCAL_CONFIG["USE_LOCAL_AGENT"]
    
    new_mode = "local" if LOCAL_CONFIG["USE_LOCAL_AGENT"] else "remote"
    logger.info(f"Switched to {new_mode} mode")
    
    return {
        "mode": new_mode,
        "message": f"Switched to {new_mode} mode",
        "agent_available": local_agent_available
    }

@app.get("/debug")
async def debug_info():
    """Debug information endpoint"""
    if not LOCAL_CONFIG["DEBUG_MODE"]:
        raise HTTPException(status_code=404, detail="Debug mode disabled")
    
    return {
        "config": LOCAL_CONFIG,
        "digital_roots_path": DIGITAL_ROOTS_PATH,
        "digital_roots_exists": os.path.exists(DIGITAL_ROOTS_PATH),
        "local_agent_available": local_agent_available,
        "local_agent_type": type(local_agent).__name__ if local_agent else None,
        "python_path": sys.path[:3],  # First few entries
        "environment_variables": {
            k: v for k, v in os.environ.items() 
            if k.startswith(('DR_', 'DIGITAL_', 'ASSISTANT_', 'USE_', 'DEBUG'))
        }
    }

# Mount static files (CSS, JS, images if any)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("?? Starting GHC Digital Twin Local Development Server")
    print(f"?? Digital Roots Path: {DIGITAL_ROOTS_PATH}")
    print(f"?? Digital Roots Available: {local_agent_available}")
    print(f"?? Mode: {'Local Agent' if LOCAL_CONFIG['USE_LOCAL_AGENT'] and local_agent_available else 'Remote API'}")
    print(f"?? Server starting at: http://{LOCAL_CONFIG['HOST']}:{LOCAL_CONFIG['PORT']}")
    print(f"?? Debug Mode: {LOCAL_CONFIG['DEBUG_MODE']}")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(
        app, 
        host=LOCAL_CONFIG['HOST'], 
        port=LOCAL_CONFIG['PORT'], 
        reload=os.getenv('AUTO_RELOAD', 'true').lower() == 'true',
        log_level="debug" if LOCAL_CONFIG['DEBUG_MODE'] else "info"
    )