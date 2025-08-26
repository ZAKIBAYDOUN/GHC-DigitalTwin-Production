@echo off
echo.
echo ========================================
echo  GHC Digital Twin - Local Development
echo ========================================
echo.
echo Starting local development server...
echo.
echo Checking dependencies...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

REM Check if digital-roots directory exists
if not exist "C:\Users\zakib\source\repos\ZAKIBAYDOUN\digital-roots" (
    echo WARNING: digital-roots repository not found at expected location
    echo Expected: C:\Users\zakib\source\repos\ZAKIBAYDOUN\digital-roots
    echo The server will run in remote-only mode
    echo.
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating requirements...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

REM Create .env from example if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env >nul
    )
)

echo.
echo ========================================
echo Server will start at: http://localhost:8000
echo.
echo Available endpoints:
echo - http://localhost:8000           (Main app)
echo - http://localhost:8000/health    (Health check)
echo - http://localhost:8000/config    (Configuration)
echo - http://localhost:8000/debug     (Debug info)
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server
echo Starting server...
start /B python local_server.py

REM Wait a moment for server to start, then run tests
timeout /t 3 >nul
echo.
echo Running connectivity tests...
python test_local.py --wait

echo.
echo ========================================
echo Server is running! Open your browser to:
echo http://localhost:8000
echo ========================================
echo.
echo Press any key to stop the server...
pause >nul

REM Kill the server process
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo Server stopped.
pause