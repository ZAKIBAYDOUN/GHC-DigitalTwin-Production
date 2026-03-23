"""
GHC Digital Twin - Tool Implementations
Each function is a tool that the agent can execute.
Uses in-memory storage for session state, approvals, and evidence.
"""
import json
from datetime import datetime
from typing import Any, Dict, List
import uuid

# The canonical list of tool definitions.
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "status_get",
            "description": "Return cockpit snapshot: counts, last actions, pending approvals.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_search",
            "description": "Search local knowledge vault for top-k results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5, "minimum": 1, "maximum": 10},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_ingest_request",
            "description": "Register an ingest request (never writes): normalize file/text for later approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "filename or 'inline-text'"},
                    "note": {"type": "string"},
                },
                "required": ["source"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "approvals_add",
            "description": "Add a pending approval item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "link": {"type": "string"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "approvals_mark",
            "description": "Mark an approval item as Approved/Denied.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "status": {"type": "string", "enum": ["Approved", "Denied"]},
                },
                "required": ["id", "status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evidence_log",
            "description": "Append a structured evidence record (event, payload).",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {"type": "string"},
                    "payload": {"type": "object", "additionalProperties": True},
                },
                "required": ["event"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "codex_prompt_build",
            "description": "Return a pre-filled Code Agent block for maintenance/upgrade or run/start.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string"},
                    "action_notes": {"type": "string"},
                    "run": {"type": "boolean", "default": True},
                    "change_id": {"type": "string"},
                },
                "required": ["goal", "action_notes", "change_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "state_get",
            "description": "Read Session Anchors (phase, last_actions, pending_approvals, key_dates).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "state_update",
            "description": "Update Session Anchors fields.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phase": {"type": "string"},
                    "key_dates": {
                        "type": "object",
                        "properties": {
                            "zec_filing": {"type": "string"},
                            "gmp_dossier": {"type": "string"},
                            "cash_buffer_to": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
]

# --- In-memory stores ---

_approvals: List[Dict[str, Any]] = []
_evidence_log: List[Dict[str, Any]] = []
_ingest_requests: List[Dict[str, Any]] = []
_last_actions: List[str] = []

_session_state: Dict[str, Any] = {
    "phase": "operational",
    "last_actions": [],
    "pending_approvals": 0,
    "key_dates": {
        "zec_filing": "",
        "gmp_dossier": "",
        "cash_buffer_to": "",
    },
}

# Built-in knowledge entries for vault search
_knowledge_vault: List[Dict[str, Any]] = [
    {"id": "k1", "text": "Green Hill Canarias operates 750 hectares of sustainable farmland in the Canary Islands.", "domain": "operations"},
    {"id": "k2", "text": "Q3 2024 revenue reached EUR 3.2M with 32% year-over-year growth.", "domain": "financial"},
    {"id": "k3", "text": "Series A funding target is EUR 8M for technology expansion and market growth.", "domain": "financial"},
    {"id": "k4", "text": "The company employs 180+ staff including 45 engineers focused on precision agriculture.", "domain": "operations"},
    {"id": "k5", "text": "Carbon-neutral operations achieved in Q4 2024 through renewable energy and sustainable practices.", "domain": "sustainability"},
    {"id": "k6", "text": "Water usage reduced by 30% through smart IoT-based irrigation systems.", "domain": "sustainability"},
    {"id": "k7", "text": "EBITDA margin at 22% and improving, with operating cash flow positive since Q2 2024.", "domain": "financial"},
    {"id": "k8", "text": "Market expansion planned for mainland Spain and North Africa in 2025.", "domain": "strategic"},
    {"id": "k9", "text": "98.5% quality certification rate across all agricultural products.", "domain": "operations"},
    {"id": "k10", "text": "ZEC (Zona Especial Canaria) tax incentives provide 4% corporate tax rate.", "domain": "compliance"},
    {"id": "k11", "text": "Supply chain includes 15 distribution partners across Europe.", "domain": "operations"},
    {"id": "k12", "text": "Biodiversity increased by 40% through regenerative farming practices.", "domain": "sustainability"},
]


# --- Tool Implementations ---


def status_get() -> Dict[str, Any]:
    pending = [a for a in _approvals if a["status"] == "pending"]
    return {
        "status": "ok",
        "counts": {
            "approvals_pending": len(pending),
            "approvals_total": len(_approvals),
            "evidence_entries": len(_evidence_log),
            "ingest_requests": len(_ingest_requests),
            "knowledge_items": len(_knowledge_vault),
        },
        "last_actions": _last_actions[-5:],
        "pending_approvals": [
            {"id": a["id"], "title": a["title"]} for a in pending
        ],
        "timestamp": datetime.now().isoformat(),
    }


def vault_search(query: str, k: int = 5) -> Dict[str, Any]:
    query_lower = query.lower()
    scored = []
    for entry in _knowledge_vault:
        text_lower = entry["text"].lower()
        score = sum(1 for word in query_lower.split() if word in text_lower)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [
        {"id": e["id"], "text": e["text"], "domain": e["domain"], "score": s}
        for s, e in scored[:k]
    ]
    _last_actions.append(f"vault_search: '{query}' ({len(results)} results)")
    return {"status": "ok", "query": query, "k": k, "results": results}


def vault_ingest_request(source: str, note: str = None) -> Dict[str, Any]:
    request_id = str(uuid.uuid4())[:8]
    entry = {
        "id": request_id,
        "source": source,
        "note": note,
        "status": "pending_approval",
        "created_at": datetime.now().isoformat(),
    }
    _ingest_requests.append(entry)
    # Auto-create an approval item
    approvals_add(title=f"Ingest: {source}", link=f"ingest://{request_id}")
    _last_actions.append(f"vault_ingest_request: {source}")
    return {"status": "ok", "request_id": request_id, "source": source, "note": note}


def approvals_add(title: str, link: str = None) -> Dict[str, Any]:
    approval_id = str(uuid.uuid4())[:8]
    entry = {
        "id": approval_id,
        "title": title,
        "link": link,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    _approvals.append(entry)
    _session_state["pending_approvals"] = len(
        [a for a in _approvals if a["status"] == "pending"]
    )
    _last_actions.append(f"approvals_add: {title}")
    return {"status": "ok", "id": approval_id, "title": title, "link": link}


def approvals_mark(id: str, status: str) -> Dict[str, Any]:
    for approval in _approvals:
        if approval["id"] == id:
            approval["status"] = status.lower()
            approval["resolved_at"] = datetime.now().isoformat()
            _session_state["pending_approvals"] = len(
                [a for a in _approvals if a["status"] == "pending"]
            )
            _last_actions.append(f"approvals_mark: {id} -> {status}")
            return {"status": "ok", "id": id, "marked_as": status}
    return {"status": "error", "message": f"Approval '{id}' not found"}


def evidence_log(event: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
    entry = {
        "id": str(uuid.uuid4())[:8],
        "event": event,
        "payload": payload or {},
        "timestamp": datetime.now().isoformat(),
    }
    _evidence_log.append(entry)
    _last_actions.append(f"evidence_log: {event}")
    return {"status": "ok", "id": entry["id"], "event": event, "payload": payload}


def codex_prompt_build(
    goal: str, action_notes: str, change_id: str, run: bool = True
) -> Dict[str, Any]:
    prompt_block = {
        "type": "code_agent_block",
        "change_id": change_id,
        "goal": goal,
        "action_notes": action_notes,
        "run": run,
        "template": f"# Change: {change_id}\n# Goal: {goal}\n# Notes: {action_notes}\n# Auto-run: {run}\n",
    }
    _last_actions.append(f"codex_prompt_build: {change_id}")
    return {"status": "ok", "prompt": prompt_block}


def state_get() -> Dict[str, Any]:
    return {
        "status": "ok",
        "phase": _session_state["phase"],
        "last_actions": _session_state.get("last_actions", _last_actions[-5:]),
        "pending_approvals": _session_state["pending_approvals"],
        "key_dates": _session_state["key_dates"],
    }


def state_update(
    phase: str = None, key_dates: Dict[str, Any] = None
) -> Dict[str, Any]:
    updated = []
    if phase is not None:
        _session_state["phase"] = phase
        updated.append("phase")
    if key_dates is not None:
        for k, v in key_dates.items():
            if k in _session_state["key_dates"]:
                _session_state["key_dates"][k] = v
                updated.append(f"key_dates.{k}")
    _last_actions.append(f"state_update: {updated}")
    return {"status": "ok", "updated_fields": updated, "current_state": _session_state}


# --- Tool Dispatcher ---

TOOL_IMPLEMENTATIONS = {
    "status_get": status_get,
    "vault_search": vault_search,
    "vault_ingest_request": vault_ingest_request,
    "approvals_add": approvals_add,
    "approvals_mark": approvals_mark,
    "evidence_log": evidence_log,
    "codex_prompt_build": codex_prompt_build,
    "state_get": state_get,
    "state_update": state_update,
}


def get_tool_definitions() -> List[Dict[str, Any]]:
    """Returns the list of all tool definitions."""
    return TOOL_DEFINITIONS


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Executes a tool by its name with the given arguments."""
    if name not in TOOL_IMPLEMENTATIONS:
        return {"error": f"Tool '{name}' not found."}

    tool_function = TOOL_IMPLEMENTATIONS[name]

    try:
        result = tool_function(**args)
        return {"tool_name": name, "result": result}
    except TypeError as e:
        return {"error": f"Invalid arguments for tool '{name}': {e}"}
    except Exception as e:
        return {"error": f"Error executing tool '{name}': {e}"}
