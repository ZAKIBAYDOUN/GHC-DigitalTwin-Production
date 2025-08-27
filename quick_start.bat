@echo off
echo Starting GHC Digital Twin Live System...
echo.

REM Quick dependency check
py -c "import fastapi, uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo Installing FastAPI...
    py -m pip install fastapi uvicorn python-dotenv httpx
)

echo Starting server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server directly
py -m uvicorn digital_twin_live:app --host 0.0.0.0 --port 8000