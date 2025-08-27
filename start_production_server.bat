@echo off
title GHC Digital Twin Live System

echo.
echo ====================================================
echo   GHC DIGITAL TWIN - LIVE SYSTEM ACTIVATED
echo   Real LangGraph Cloud Integration
echo ====================================================
echo.

REM Check if server is already running
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo Server already running on port 8000
    echo Opening browser...
    start http://localhost:8000
    pause
    exit /b 0
)

echo Starting GHC Digital Twin Live System...
echo LangGraph Cloud: ENABLED
echo Real AI Agents: 10 specialized agents ready
echo.

REM Start server using uvicorn for better stability
py -m uvicorn digital_twin_live:app --host 0.0.0.0 --port 8000 --log-level info

pause