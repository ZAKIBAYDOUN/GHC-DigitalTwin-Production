#!/bin/bash

echo "=================================================="
echo "   GREEN HILL CANARIAS - DIGITAL TWIN DEPLOY"
echo "=================================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Create directories
mkdir -p data logs static

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Installing basic requirements..."
    pip install fastapi uvicorn python-dotenv requests pydantic
fi

# Setup environment file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "? Created .env from example"
    else
        cat > .env << EOF
DR_BASE_URL=https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app
DR_API_KEY=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
HOST=0.0.0.0
PORT=8000
EOF
        echo "? Created basic .env file"
    fi
fi

echo
echo "?? Starting Digital Twin System..."
echo "?? Access at: http://localhost:8000"
echo

# Start the system
if [ -f "simple_digital_twin.py" ]; then
    python simple_digital_twin.py
elif [ -f "api/server.py" ]; then
    cd api && python server.py
else
    echo "ERROR: No startup script found"
    exit 1
fi