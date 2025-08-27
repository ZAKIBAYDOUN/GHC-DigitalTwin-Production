# ?? GHC Digital Twin - API Keys Setup Guide

## ?? Required API Keys

To fully activate your GHC Digital Twin live system with LangGraph deployment, you need:

### 1. OpenAI API Key
- **Purpose**: Powers the AI language models
- **Get it from**: https://platform.openai.com/api-keys
- **Format**: `sk-...` (starts with "sk-")
- **Cost**: Pay-per-use (very affordable for business use)

**Steps:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Replace `sk-your-openai-api-key-here` in your `.env` file

### 2. LangSmith API Key
- **Purpose**: Enables tracing and monitoring of your AI agents
- **Get it from**: https://smith.langchain.com/
- **Format**: `lsv2_sk_...` or similar
- **Cost**: Free tier available

**Steps:**
1. Go to https://smith.langchain.com/
2. Sign in with your LangChain account
3. Go to Settings ? API Keys
4. Create a new API key
5. Replace `your-langsmith-api-key-here` in your `.env` file

## ?? Your LangGraph Deployment

Your live deployment is configured at:
**https://dgt-1bf5f8c56c9c5dcd9516a1ba62c5ebf1.us.langgraph.app**

This deployment includes:
- ? Real AI agent workflows
- ? Multi-agent collaboration  
- ? Company-specific knowledge
- ? Executive decision support

## ?? Quick Setup

1. **Get your OpenAI API key:**
   ```bash
   # Visit: https://platform.openai.com/api-keys
   # Copy your key (starts with sk-)
   ```

2. **Get your LangSmith API key:**
   ```bash
   # Visit: https://smith.langchain.com/
   # Go to Settings ? API Keys
   # Create and copy new key
   ```

3. **Update your `.env` file:**
   ```env
   OPENAI_API_KEY="sk-your-actual-openai-key-here"
   LANGSMITH_API_KEY="your-actual-langsmith-key-here"
   LANGCHAIN_API_KEY="your-actual-langsmith-key-here"
   ```

4. **Start your system:**
   ```bash
   py start_langgraph_live.bat
   ```

## ?? Benefits of Full Setup

With proper API keys, you get:

### ?? Real AI Agents
- CEO Digital Twin with strategic insights
- CFO Agent for financial analysis  
- Agricultural Intelligence for crop optimization
- Sustainability Agent for ESG metrics
- And 6 more specialized agents

### ?? Advanced Capabilities
- Natural language understanding
- Complex reasoning and analysis
- Multi-agent collaboration
- Real-time decision support

### ?? Monitoring & Analytics
- Request tracing with LangSmith
- Performance monitoring
- Usage analytics
- Error tracking

### ?? Executive Features
- Boardroom-level insights
- Investor presentation support
- Public communication assistance
- Strategic planning support

## ?? Security Notes

- Keep your API keys secure and never commit them to Git
- The `.env` file is already in `.gitignore`
- Your keys are only used for your private deployment
- All communication is encrypted (HTTPS)

## ? Quick Start Commands

```bash
# 1. Update your .env file with real API keys
notepad .env

# 2. Start the live system
py start_langgraph_live.bat

# 3. Test the system  
py test_production.py

# 4. Open in browser
start http://localhost:8000
```

## ?? Ready to Go!

Once you've added your API keys, your GHC Digital Twin will have:
- ? Real AI-powered responses
- ? Company-specific knowledge 
- ? Executive-level insights
- ? Multi-agent collaboration
- ? Production-ready performance

Your digital twin is ready to provide strategic insights for Green Hill Canarias! ??