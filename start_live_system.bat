@echo off
echo.
echo ====================================================
echo   GREEN HILL CANARIAS - DIGITAL TWIN LIVE SYSTEM
echo   Activating Real AI Agents with LangGraph
echo ====================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "static" mkdir static

echo ? Directories verified

REM Setup virtual environment
if not exist "venv" (
    echo ?? Creating virtual environment...
    python -m venv venv
)

echo ?? Activating virtual environment...
call venv\Scripts\activate.bat

echo ?? Installing/updating requirements...
pip install --upgrade pip
pip install -r requirements.txt

REM Check .env configuration
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ??  Created .env from example - Please configure your API keys!
    ) else (
        echo ? No .env file found. Please create one with your API keys.
        pause
        exit /b 1
    )
)

echo.
echo ====================================================
echo      ?? LAUNCHING LIVE DIGITAL TWIN SYSTEM
echo ====================================================
echo.
echo ?? System Features:
echo    ? 10 Specialized AI Agents
echo    ? LangGraph Integration
echo    ? Real-time Knowledge Base
echo    ? Multi-agent Collaboration
echo    ? Enhanced Analytics
echo.
echo ?? Access Points:
echo    • Dashboard: http://localhost:8000
echo    • API Docs:  http://localhost:8000/docs
echo    • Health:    http://localhost:8000/api/system/health
echo.
echo ?? System Status will be displayed below...
echo.

REM Start the live system
python digital_twin_live.py

pause