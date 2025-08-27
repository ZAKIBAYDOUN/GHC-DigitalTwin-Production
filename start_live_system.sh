#!/bin/bash

echo "===================================================="
echo "  GREEN HILL CANARIAS - DIGITAL TWIN LIVE SYSTEM"
echo "  Activating Real AI Agents with LangGraph"
echo "===================================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "? ERROR: Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Create directories
mkdir -p data logs static
echo "? Directories verified"

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "?? Creating virtual environment..."
    python3 -m venv venv
fi

echo "?? Activating virtual environment..."
source venv/bin/activate

echo "?? Installing/updating requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Check .env configuration
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "??  Created .env from example - Please configure your API keys!"
    else
        echo "? No .env file found. Please create one with your API keys."
        exit 1
    fi
fi

echo
echo "===================================================="
echo "     ?? LAUNCHING LIVE DIGITAL TWIN SYSTEM"
echo "===================================================="
echo
echo "?? System Features:"
echo "   ? 10 Specialized AI Agents"
echo "   ? LangGraph Integration" 
echo "   ? Real-time Knowledge Base"
echo "   ? Multi-agent Collaboration"
echo "   ? Enhanced Analytics"
echo
echo "?? Access Points:"
echo "   • Dashboard: http://localhost:8000"
echo "   • API Docs:  http://localhost:8000/docs"
echo "   • Health:    http://localhost:8000/api/system/health"
echo
echo "?? System Status will be displayed below..."
echo

# Start the live system
python digital_twin_live.py