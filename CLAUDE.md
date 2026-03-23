# CLAUDE.md — GHC Digital Twin Production

## Project Overview

**GHC Digital Twin** is a full-stack AI-powered digital twin system for **Green Hill Canarias**, a sustainable agriculture operation in the Canary Islands (750 hectares, 180+ employees). The system provides real-time monitoring, analytics, and AI-driven decision support through a 10-agent ecosystem orchestrated via LangGraph Cloud.

**Tech Stack:**
- **Backend:** Python 3.11, FastAPI, LangGraph/LangChain, LangSmith
- **Frontend:** Next.js 14, React 18, TypeScript, Tailwind CSS
- **Dashboard:** Streamlit
- **Database:** ChromaDB (vector store), PostgreSQL (optional)
- **Deployment:** Docker, Vercel, Netlify, GitHub Pages, Heroku

---

## Repository Structure

```
GHC-DigitalTwin-Production/
├── api/                        # FastAPI backend
│   ├── server.py               # Main REST API (endpoints, CORS, routing)
│   ├── graph.py                # LangGraph Cloud integration (async streaming)
│   ├── tools.py                # AI tool definitions (8 tools)
│   ├── uvicorn_app.py          # ASGI entry point
│   ├── requirements.txt        # Python dependencies
│   └── pyproject.toml          # Black & isort config
├── frontend/                   # Next.js 14 frontend
│   ├── src/pages/index.tsx     # Main React component
│   ├── package.json            # Node dependencies & scripts
│   ├── tsconfig.json           # TypeScript config (strict: false)
│   ├── tailwind.config.js      # Tailwind CSS config
│   └── Dockerfile              # Frontend container (node:18-alpine)
├── tests/                      # Test suites
│   ├── test_local.py           # Local endpoint tests
│   ├── test_endpoints.py       # Async endpoint tests
│   └── test_deployment.py      # Deployment verification
├── docs/                       # Architecture & deployment docs
│   ├── DIGITAL_TWIN_ARCHITECTURE.md
│   ├── DEPLOYMENT_COMPLETE.md
│   └── QUICKSTART.md
├── scripts/                    # Utility scripts (Windows batch)
├── web/                        # Static web assets
├── .github/workflows/deploy.yml # CI/CD (GitHub Pages)
├── config.js                   # LangGraph deployment config
├── langgraph.json              # LangGraph metadata
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Backend container (python:3.11-slim)
├── Makefile                    # Development shortcuts
├── Procfile                    # Heroku config
├── netlify.toml                # Netlify config
├── vercel.json                 # Vercel config
├── simple_digital_twin.py      # Lightweight production server
├── enhanced_digital_twin.py    # Full-featured server (with Chroma)
├── digital_twin_live.py        # Live streaming server
├── streamlit_app.py            # Streamlit dashboard
├── main.py                     # Core application logic
├── local_server.py             # Local development server
└── .env.example                # Environment variable template
```

---

## Development Setup

### Prerequisites
- Python 3.8+ (3.11 recommended)
- Node.js 18+
- Docker & Docker Compose (optional)

### Backend
```bash
cd api
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp ../.env.example ../.env  # Configure environment variables
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev     # Development server on port 3000
```

### Streamlit Dashboard
```bash
streamlit run streamlit_app.py  # Runs on port 8501
```

### Docker
```bash
docker-compose up  # Backend on :8000, Frontend on :3000
```

---

## Key Commands

### Makefile Targets
| Command      | Action                                          |
|--------------|-------------------------------------------------|
| `make be`    | Start backend (uvicorn on port 8000 with reload)|
| `make fe`    | Start frontend dev server                       |
| `make fmt`   | Format Python code with Black                   |
| `make recover` | Dump data from LangGraph deployment           |
| `make check` | Show usage info                                 |

### Frontend Scripts (package.json)
| Command         | Action                  |
|-----------------|-------------------------|
| `npm run dev`   | Next.js dev server      |
| `npm run build` | Production build        |
| `npm run start` | Production server       |

### Formatting
```bash
black api/          # Python formatter (line-length: 88)
```

---

## Architecture

### Request Flow
```
User → Frontend (Next.js / Streamlit / HTML) → FastAPI (/api/ask) → LangGraph Cloud → AI Agents → Response
```

The backend acts as a **proxy** to LangGraph Cloud. It receives user questions, routes them to the appropriate LangGraph assistant based on audience type, and returns the processed response.

### Audience Types
Three audience-specific assistants with dedicated LangGraph assistant IDs:
- **boardroom** — Executive-level strategic insights
- **investor** — Financial data with citations (citations required)
- **public** — General-purpose information

### 10-Agent Ecosystem
| Agent | Domain |
|-------|--------|
| CEO Digital Twin | Strategic oversight & decision-making |
| CFO Agent | Financial analysis & planning |
| COO Agent | Operations optimization |
| CMO Agent | Marketing & customer insights |
| Agricultural Intelligence | Crop monitoring & optimization |
| Sustainability Agent | Environmental impact & ESG metrics |
| Risk Management | Risk assessment & mitigation |
| Compliance Agent | Regulatory governance |
| Data Analytics | Data processing & insights |
| Customer Service | Support & relationship management |

### 8 Core Tools
`status_get`, `vault_search`, `vault_ingest_request`, `approvals_add`, `approvals_mark`, `evidence_log`, `codex_prompt_build`, `state_get`/`state_update`

---

## API Endpoints

All endpoints are defined in `api/server.py`.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Basic health check |
| `/api/system/health` | GET | System status with agent count |
| `/api/ask` | POST | Main chat (accepts `{audience, question}`) |
| `/api/history` | GET | Chat history |
| `/api/agents` | GET | List available agents |
| `/api/tools` | GET | List tool definitions |
| `/api/tools/execute` | POST | Execute a tool (`{name, args}`) |
| `/api/ingest` | POST | Document ingestion |
| `/board/answer` | POST | Boardroom-specific endpoint |
| `/investor/answer` | POST | Investor-specific (requires citations) |
| `/public/answer` | POST | Public-facing endpoint |

CORS is configured to allow all origins.

---

## Code Conventions

### Python
- **Formatter:** Black (line-length: 88), configured in `api/pyproject.toml`
- **Import sorting:** isort with `profile = "black"`
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
- **Type hints:** Used in Pydantic models; not enforced elsewhere
- **Async:** Heavy use of `async/await` for LangGraph integration

### TypeScript / Frontend
- **Framework:** Next.js 14 pages router (`src/pages/`)
- **Styling:** Tailwind CSS utility classes
- **TypeScript:** `strict: false` in tsconfig
- **Components:** React hooks pattern (`useState`, `useEffect`)

### Git Conventions
- **Commit messages:** Present tense, imperative mood ("Add feature" not "Added feature")
- **First line:** Max 72 characters
- **Branch naming:** `claude/<description>-<ID>` for AI-generated branches

---

## Testing

Tests use HTTP requests to verify endpoint availability and responses. No formal test framework (pytest/unittest) is configured.

```bash
python tests/test_local.py         # Local endpoint tests
python tests/test_endpoints.py     # Async endpoint tests
python tests/test_deployment.py    # Deployment verification
python test_production.py          # Root-level production test
python simple_test.py              # Quick smoke test
```

---

## Environment Variables

Reference `.env.example` for the full template. Key variables:

| Variable | Purpose |
|----------|---------|
| `LANGGRAPH_DEPLOYMENT_URL` | LangGraph Cloud endpoint |
| `DR_API_KEY` | LangGraph/LangSmith API key |
| `OPENAI_API_KEY` | OpenAI API (embeddings, LLM) |
| `LANGSMITH_API_KEY` | LangSmith tracing |
| `ASSISTANT_ID_BOARDROOM` | Boardroom assistant UUID |
| `ASSISTANT_ID_INVESTOR` | Investor assistant UUID |
| `ASSISTANT_ID_PUBLIC` | Public assistant UUID |
| `USE_LOCAL_AGENT` | Use local agent instead of cloud |
| `DEBUG_MODE` | Enable debug logging |
| `VECTORSTORE_DIR` | ChromaDB storage path (`./data/chroma`) |

**Never commit actual API keys.** Use `.env` (gitignored) or deployment secrets.

---

## Deployment

| Platform | Config File | Notes |
|----------|-------------|-------|
| Docker | `docker-compose.yml`, `Dockerfile` | Backend :8000, Frontend :3000 |
| Vercel | `vercel.json` | Python backend + Next.js frontend |
| Netlify | `netlify.toml` | Frontend builds from `frontend/.next` |
| GitHub Pages | `.github/workflows/deploy.yml` | Static demo, auto-deploys on push to `main` |
| Heroku | `Procfile` | Runs `simple_digital_twin.py` |

### Ports
| Service | Port |
|---------|------|
| Backend API | 8000 |
| Frontend (Next.js) | 3000 |
| Streamlit Dashboard | 8501 |

---

## Important Files (Quick Reference)

- `api/server.py` — All API endpoints and routing
- `api/graph.py` — LangGraph Cloud connection and streaming
- `api/tools.py` — Tool definitions for AI agents
- `frontend/src/pages/index.tsx` — Main frontend component
- `simple_digital_twin.py` — Production entry point (default)
- `streamlit_app.py` — Interactive dashboard
- `config.js` — LangGraph agent mappings and company context
- `.env.example` — Environment variable template
- `docker-compose.yml` — Container orchestration
- `docs/DIGITAL_TWIN_ARCHITECTURE.md` — Full architecture documentation
