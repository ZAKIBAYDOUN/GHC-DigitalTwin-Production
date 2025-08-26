# GHC Digital Twin Production System

A comprehensive digital twin system with real-time monitoring, analytics, and web interfaces.

## 🏗️ Project Structure

```
GHC-DigitalTwin-Production/
├── api/                    # Backend API services
├── frontend/              # Next.js frontend application
├── web/                   # Static web assets
├── .github/               # GitHub Actions workflows
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
1. Navigate to the API directory:
   ```bash
   cd api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

5. Start the backend server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Full System Launch
Use the provided batch scripts for Windows:
```bash
# For local development
run_local.bat

# For digital twin system
run_digital_twin.bat

# Complete system startup
start_system.bat
```

## 📊 Features

- **Real-time Digital Twin**: Live system monitoring and simulation
- **Web Dashboard**: Interactive Streamlit-based interface
- **RESTful API**: Comprehensive backend services
- **Modern Frontend**: Next.js with TypeScript and Tailwind CSS
- **Automated Testing**: Comprehensive test suites
- **Deployment Ready**: Production-ready configuration

## 🔧 Development

### Running Tests
```bash
# Backend tests
python test_endpoints.py
python test_local.py
python test_deployment.py

# Frontend tests
cd frontend && npm test
```

### Code Formatting
```bash
# Python (using Black)
black api/

# Frontend (using Prettier)
cd frontend && npm run format
```

## 📚 Documentation

- [Local Development Guide](LOCAL_DEVELOPMENT.md)
- [Deployment Guide](DEPLOYMENT_COMPLETE.md)
- [Architecture Overview](DIGITAL_TWIN_ARCHITECTURE.md)
- [Quick Start Guide](QUICKSTART.md)

## 🌐 Endpoints

### API Health Check
```
GET http://localhost:8000/api/health
```

### Streamlit Dashboard
```
http://localhost:8501
```

### Frontend Application
```
http://localhost:3000
```

## 📄 License

This project is proprietary software developed for GHC Digital Twin Production System.

## 🤝 Contributing

Please refer to the development guidelines in the documentation before contributing.

---

*System Status: ✅ Production Ready*
