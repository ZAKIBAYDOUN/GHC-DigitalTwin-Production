// LangGraph Deployment Configuration for GHC Digital Twin
const LANGGRAPH_CONFIG = {
    // Your live deployment URL
    deployment_url: 'https://dgt-1bf5f8c56c9c5dcd9516a1ba62c5ebf1.us.langgraph.app',
    
    // API Key for authentication
    api_key: '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',
    
    // Assistant IDs from your deployment
    assistants: {
        boardroom: '76f94782-5f1d-4ea0-8e69-294da3e1aefb',
        investor: 'ff7afd85-51e0-4fdd-8ec5-a14508a100f9', 
        public: '34747e20-39db-415e-bd80-597006f71a7a'
    },
    
    // Agent type to assistant ID mapping
    agent_assistants: {
        'ceo_digital_twin': '34747e20-39db-415e-bd80-597006f71a7a',
        'cfo_agent': 'ff7afd85-51e0-4fdd-8ec5-a14508a100f9',
        'coo_agent': '76f94782-5f1d-4ea0-8e69-294da3e1aefb',
        'agricultural_intelligence': '34747e20-39db-415e-bd80-597006f71a7a',
        'sustainability_agent': '34747e20-39db-415e-bd80-597006f71a7a'
    },
    
    // LangSmith Tracing Configuration
    tracing: {
        enabled: true,
        project_name: 'ghc-digital-twin',
        api_endpoint: 'https://api.smith.langchain.com'
    },
    
    // Request settings
    request_settings: {
        timeout: 60000, // 60 seconds
        retry_attempts: 2,
        stream_mode: 'values'
    },
    
    // Company context for agents
    company_context: {
        name: 'Green Hill Canarias',
        industry: 'Sustainable Agriculture',
        location: 'Canary Islands',
        revenue: '3.2M EUR (Q3 2024)',
        growth: '32% YoY',
        hectares: 750,
        employees: 180
    }
};

// Export for global use
if (typeof window !== 'undefined') {
    window.LANGGRAPH_CONFIG = LANGGRAPH_CONFIG;
}

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LANGGRAPH_CONFIG;
}