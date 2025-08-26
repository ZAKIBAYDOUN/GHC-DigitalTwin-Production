@echo off
echo.
echo ========================================
echo    GHC DIGITAL TWIN - STARTUP DASHBOARD
echo    10-Agent Sophisticated System
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

REM Create directories for knowledge system
if not exist "data" mkdir data
if not exist "data\chroma" mkdir data\chroma
if not exist "data\chroma\financial" mkdir data\chroma\financial
if not exist "data\chroma\operations" mkdir data\chroma\operations
if not exist "data\chroma\compliance" mkdir data\chroma\compliance
if not exist "data\chroma\market_intelligence" mkdir data\chroma\market_intelligence
if not exist "data\chroma\sustainability" mkdir data\chroma\sustainability
if not exist "data\chroma\customer_data" mkdir data\chroma\customer_data
if not exist "data\chroma\strategic" mkdir data\chroma\strategic

REM Create logs directory
if not exist "logs" mkdir logs

echo ? Directory structure created

REM Setup virtual environment
if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing enhanced requirements...
pip install -r requirements_enhanced.txt

REM Create .env from example if needed
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ? Created .env from example
    )
)

echo.
echo ========================================
echo         SYSTEM INITIALIZATION
echo ========================================
echo.
echo ?? Initializing 10 Specialized Agents:
echo    1. CEO Digital Twin (Strategic Oversight)
echo    2. CFO Agent (Financial Analysis)
echo    3. COO Agent (Operations Management)
echo    4. CMO Agent (Marketing Intelligence)
echo    5. Agricultural Intelligence Agent
echo    6. Sustainability Agent (ESG Metrics)
echo    7. Risk Management Agent
echo    8. Compliance Agent
echo    9. Data Analytics Agent
echo   10. Customer Service Agent
echo.
echo ?? Knowledge Management System:
echo    - Vector Database (Chroma): 7 specialized domains
echo    - Real-time Data Streams: IoT, Market, Weather
echo    - Structured Databases: CRM, ERP, Financial
echo    - External APIs: Market Data, Compliance Feeds
echo.
echo ?? Agent Orchestration:
echo    - Intelligent agent selection
echo    - Multi-agent collaboration workflows
echo    - Knowledge synthesis and reasoning
echo    - Action recommendation engine
echo.

echo Starting Enhanced Digital Twin System...
echo.
echo Available at: http://localhost:8000
echo.
echo API Endpoints:
echo - POST /api/chat                (Main agent interaction)
echo - GET  /api/agents             (List all agents)
echo - POST /api/knowledge/ingest   (Add knowledge)
echo - GET  /api/knowledge/stats    (Knowledge statistics)
echo - GET  /api/system/health      (System health)
echo.

REM Start the enhanced system
python enhanced_digital_twin.py

echo.
echo System stopped.
pause