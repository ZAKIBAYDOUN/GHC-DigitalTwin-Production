# Contributing to GHC Digital Twin Production System

Thank you for your interest in contributing to the GHC Digital Twin Production System! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Git
- A code editor (VS Code recommended)

### Local Development
1. Clone the repository
2. Set up the Python environment:
   ```bash
   cd api
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Code Style

### Python
- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write docstrings for all public functions

### TypeScript/JavaScript
- Use Prettier for formatting
- Follow established ESLint rules
- Use TypeScript for type safety
- Write JSDoc comments for complex functions

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when applicable

Example:
```
Add digital twin monitoring endpoint

- Implement real-time data collection
- Add WebSocket support for live updates
- Include error handling and logging
- Update API documentation

Fixes #123
```

## Testing

### Backend Tests
```bash
python test_endpoints.py
python test_local.py
python test_deployment.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if needed
3. Add appropriate commit messages
4. Create a pull request with:
   - Clear description of changes
   - Screenshots if UI changes
   - Testing instructions
   - Reference to related issues

## Issues and Bug Reports

When creating an issue, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, Node version)
- Relevant logs or error messages

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search existing issues
3. Create a new issue with the "question" label

Thank you for contributing!