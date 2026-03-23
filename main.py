"""
GHC Digital Twin - Main Application
Green Hill Canarias API Proxy to LangGraph Cloud
"""
import os
import re
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
DR_BASE_URL = os.getenv(
    "DR_BASE_URL",
    "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app",
)
DR_API_KEY = os.getenv("DR_API_KEY", "")
PORT = int(os.getenv("PORT", "8000"))

HEADERS = {"x-api-key": DR_API_KEY, "Content-Type": "application/json"} if DR_API_KEY else {}

ASSISTANT_IDS: Dict[str, str] = {
    "boardroom": os.getenv("ASSISTANT_ID_BOARDROOM", "76f94782-5f1d-4ea0-8e69-294da3e1aefb"),
    "investor": os.getenv("ASSISTANT_ID_INVESTOR", "ff7afd85-51e0-4fdd-8ec5-a14508a100f9"),
    "public": os.getenv("ASSISTANT_ID_PUBLIC", "34747e20-39db-415e-bd80-597006f71a7a"),
}

app = FastAPI(
    title="GHC Digital Twin Proxy",
    description="Green Hill Canarias Digital Twin API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---

class QuestionIn(BaseModel):
    question: str


class AskRequest(BaseModel):
    audience: str
    question: str


# --- Helpers ---

def _contains_sensitive_tokens(text: str) -> bool:
    if not text:
        return False
    sensitive_keywords = [
        "sha", "financial", "financials", "balance sheet",
        "income statement", "cashflow", "ssn", "secret", "salary",
    ]
    return any(k in text.lower() for k in sensitive_keywords)


def _truncate(text: str, limit: int = 800) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def _extract_answer_and_citations(resp: Any) -> Dict[str, Any]:
    """Normalize different response shapes into {answer, citations}."""
    answer = ""
    citations: List[Dict[str, str]] = []

    if isinstance(resp, dict):
        # Common text fields
        for k in ("answer", "text", "output", "result", "content"):
            if k in resp and isinstance(resp[k], str) and resp[k].strip():
                answer = resp[k].strip()
                break

        # Nested structures
        if not answer:
            for k in ("output", "results", "data", "response"):
                v = resp.get(k)
                if isinstance(v, str) and v.strip():
                    answer = v.strip()
                    break
                if isinstance(v, dict):
                    nested = _extract_answer_and_citations(v)
                    if nested.get("answer"):
                        answer = nested["answer"]
                        citations = nested.get("citations", [])
                        break
                if isinstance(v, list) and v:
                    for item in v:
                        if isinstance(item, str) and item.strip():
                            answer = item.strip()
                            break
                        if isinstance(item, dict):
                            nested = _extract_answer_and_citations(item)
                            if nested.get("answer"):
                                answer = nested["answer"]
                                citations = nested.get("citations", [])
                                break
                    if answer:
                        break

        # Extract citations
        for key in ("citations", "references", "sources", "refs"):
            if key in resp and isinstance(resp[key], list):
                for c in resp[key]:
                    if isinstance(c, dict):
                        citations.append({
                            "source": c.get("source", ""),
                            "section": c.get("section", ""),
                            "clause": c.get("clause", ""),
                            "url": c.get("url", ""),
                        })
                if citations:
                    break

    return {"answer": answer or "", "citations": citations}


async def _call_runs_wait(assistant_id: str, question: str) -> Any:
    """Call LangGraph deployment and return the response."""
    if not DR_BASE_URL or not DR_API_KEY:
        return {"error": "LangGraph credentials not configured"}

    url = f"{DR_BASE_URL.rstrip('/')}/runs/wait"
    payload = {"assistant_id": assistant_id, "input": {"question": question}}
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, headers=HEADERS, json=payload)
        try:
            return resp.json()
        except Exception:
            return {"status_code": resp.status_code, "text": resp.text}


# --- Routes ---

@app.get("/")
def root():
    return {
        "message": "GHC Digital Twin API is running.",
        "docs": "/docs",
        "endpoints": [
            {"POST": "/board/answer"},
            {"POST": "/investor/answer"},
            {"POST": "/public/answer"},
            {"POST": "/api/ask"},
        ],
    }


@app.get("/api/health")
async def health():
    return {"ok": True, "status": "healthy", "version": "2.0.0"}


@app.get("/api/history")
async def history():
    return {"history": []}


@app.post("/api/ask")
async def ask(request: AskRequest):
    audience = request.audience.lower()
    if audience not in ASSISTANT_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audience. Must be one of: {list(ASSISTANT_IDS.keys())}",
        )

    if not DR_API_KEY:
        return {
            "status": "mock_response",
            "response": f"[No API key configured] Mock response for {audience}: {request.question}",
            "agent": audience,
        }

    assistant_id = ASSISTANT_IDS[audience]
    resp = await _call_runs_wait(assistant_id, request.question)
    return _extract_answer_and_citations(resp)


@app.post("/board/answer")
async def board_answer(request: Request):
    body = await request.json()
    question = body.get("question") if isinstance(body, dict) else None
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in request body")
    assistant_id = ASSISTANT_IDS["boardroom"]
    resp = await _call_runs_wait(assistant_id, question)
    return _extract_answer_and_citations(resp)


@app.post("/investor/answer")
async def investor_answer(request: Request):
    body = await request.json()
    question = body.get("question") if isinstance(body, dict) else None
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in request body")
    resp = await _call_runs_wait(ASSISTANT_IDS["investor"], question)
    normalized = _extract_answer_and_citations(resp)
    if not normalized.get("citations"):
        raise HTTPException(status_code=422, detail="Response did not include citations/references")
    if normalized.get("answer"):
        normalized["answer"] += "\n\n-- Information only; not investment advice."
    else:
        normalized["disclaimer"] = "-- Information only; not investment advice."
    return normalized


@app.post("/public/answer")
async def public_answer(request: Request):
    body = await request.json()
    question = body.get("question") if isinstance(body, dict) else None
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in request body")
    if _contains_sensitive_tokens(question):
        return {
            "answer": "This information is restricted. Please contact Investor Relations.",
            "citations": [],
        }
    resp = await _call_runs_wait(ASSISTANT_IDS["public"], question)
    normalized = _extract_answer_and_citations(resp)
    ans = normalized.get("answer", "")
    if len(ans) > 800:
        normalized["answer"] = _truncate(ans, 800)
    return normalized


@app.post("/api/ingest")
async def ingest(file: UploadFile = File(None)):
    if file is None:
        raise HTTPException(status_code=400, detail="No file provided")
    contents = await file.read()
    return {
        "status": "accepted",
        "filename": file.filename,
        "size": len(contents),
        "message": "File received for processing",
    }


@app.get("/internal/assistants")
async def internal_assistants():
    return {"DR_BASE_URL": DR_BASE_URL, "ASSISTANT_IDS": ASSISTANT_IDS}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
