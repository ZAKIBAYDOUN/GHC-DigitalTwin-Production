# GHC Digital Twin - Quick Start Guide

## ?? Quick Setup (Windows)

### Option 1: Automated Setup
```cmd
# Run the setup script
python setup_local.py

# Start the server
run_local.bat
```

### Option 2: Manual Setup
```cmd
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
copy .env.example .env

# 4. Start server
python local_server.py
```

## ?? Access Your App

Open your browser to: **http://localhost:8000**

## ?? Configuration Modes

### Local Agent Mode
- Uses your local digital-roots repository
- Path: `C:\Users\zakib\source\repos\ZAKIBAYDOUN\digital-roots`
- Faster response times
- Full debugging capabilities

### Remote API Mode  
- Uses DigitalRoots cloud service
- Fallback when local agent unavailable
- Production-like environment

## ??? Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `http://localhost:8000` | Main application |
| `http://localhost:8000/health` | Health check |
| `http://localhost:8000/config` | Current configuration |
| `http://localhost:8000/debug` | Debug information |
| `http://localhost:8000/toggle-mode` | Switch local/remote |

## ?? Testing Your Setup

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Configuration Check
```bash
curl http://localhost:8000/config
```

### 3. Test Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Green Hill Canarias?", "audience": "public"}'
```

## ?? Troubleshooting

### Server won't start
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 isn't in use

### Local agent not found
- Verify path: `C:\Users\zakib\source\repos\ZAKIBAYDOUN\digital-roots`
- Check if digital-roots has proper Python package structure
- Server will automatically fall back to remote mode

### CORS errors
- Access via `http://localhost:8000` not `file://`
- Check server console for errors

## ?? Development Workflow

1. **Frontend Changes**: Edit `index.html` or `index_local.html`
2. **Server Changes**: Edit `local_server.py` (auto-reloads)
3. **Agent Changes**: Modify files in digital-roots repository
4. **Toggle Modes**: Use debug panel or `/toggle-mode` endpoint

## ?? Debug Information

Enable debug mode in `.env`:
```
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Access debug info at: `http://localhost:8000/debug`

## ?? Need Help?

1. Check server console output
2. Visit debug endpoint
3. Test with health check endpoint
4. Verify .env configuration