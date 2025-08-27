@echo off
echo.
echo ====================================================
echo   GHC DIGITAL TWIN - LIVE SYSTEM WITH LANGGRAPH
echo ====================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create and activate virtual environment
if not exist "venv" (
    echo ?? Creating virtual environment...
    python -m venv venv
)

echo ?? Activating virtual environment...
call venv\Scripts\activate.bat

REM Check .env file
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please ensure your .env file is in the project directory
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs  
if not exist "static" mkdir static

echo ? Environment loaded
echo ? LangGraph API configured
echo ? Installing/updating dependencies...

REM Install required packages
pip install --upgrade pip
pip install fastapi uvicorn[standard] python-dotenv pydantic httpx aiofiles
pip install langgraph langchain-core langchain-openai requests

echo ? Dependencies installed
echo ? Starting server with LangGraph cloud integration...
echo.
echo ?? Server will be available at: http://localhost:8000
echo ?? API Documentation: http://localhost:8000/docs
echo ?? Real AI agents with LangGraph cloud processing
echo.

REM Start the server
python digital_twin_live.py

if %errorlevel% neq 0 (
    echo.
    echo ? Server failed to start. Trying fallback...
    echo.
    pip install -r requirements.txt
    python digital_twin_live.py
)

pause