@echo off
echo.
echo ==========================================
echo   GREEN HILL CANARIAS - DIGITAL TWIN
echo   Simplified Startup System
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create basic directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "static" mkdir static

echo ? Directories created

REM Setup virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo Installing basic requirements...
    pip install fastapi uvicorn python-dotenv requests pydantic
)

REM Check for .env file
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ? Created .env from example
    ) else (
        echo # Basic configuration > .env
        echo DR_BASE_URL=https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app >> .env
        echo DR_API_KEY=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 >> .env
        echo HOST=0.0.0.0 >> .env
        echo PORT=8000 >> .env
        echo ? Created basic .env file
    )
)

echo.
echo ==========================================
echo      DIGITAL TWIN SYSTEM STARTING
echo ==========================================
echo.
echo ?? 10 AI Agents Ready:
echo    CEO • CFO • COO • CMO • Agricultural
echo    Sustainability • Risk • Compliance 
echo    Analytics • Customer Service
echo.
echo ?? Access at: http://localhost:8000
echo.
echo API Endpoints:
echo - GET  /api/agents          (List agents)
echo - POST /api/ask             (Chat with agents) 
echo - GET  /api/system/health   (System status)
echo.

REM Start the system
if exist "simple_digital_twin.py" (
    python simple_digital_twin.py
) else if exist "api\server.py" (
    echo Starting API server...
    cd api && python server.py
) else (
    echo ERROR: No startup script found
    pause
    exit /b 1
)

pause