Physics-Constrained AI Validation
To combat AI hallucinations, FloatChat includes a scientific guardrail. Every result is cross-validated against a Climatological Database (like the World Ocean Atlas). The system doesn't just check if a value is possible; it checks if it's plausible for that specific location and time of year. This grounds the AI's responses in decades of established oceanographic science, building unparalleled trust and reliability.
Intelligent & Cost-Effective Text-to-SQL
Our hybrid engine handles ~80% of common queries with highly-optimized, hand-tuned templates for millisecond response times and near-zero cost. For novel, complex questions, it seamlessly falls back to a powerful LLM (GPT-4). A built-in EXPLAIN-based cost estimator also acts as a safety net, preventing expensive or malicious queries from impacting database performance.
Seamless Conversational UX
Vague questions like "Show me warm water near Mumbai" don't cause failure. FloatChat's Ambiguity Resolver intelligently applies sensible defaults (e.g., warm > 28°C, near = 100km radius) and presents them to you with interactive UI elements within the chat. You can adjust parameters with sliders and buttons, refining your query collaboratively without ever re-typing it.
Enterprise-Grade Data Backend
The system is powered by PostgreSQL with the TimescaleDB extension, a battle-tested solution for handling massive volumes of time-series and geospatial data. This unified architecture avoids the pitfalls of complex hybrid systems and delivers high-performance queries on a petabyte-scale data store.
System Architecture
FloatChat's final architecture (Version 3) is a multi-stage parallel processing pipeline designed for performance, accuracy, and scalability.
code
Mermaid
graph TD
    A[User Query via Streamlit UI] --> B{Conversational Ambiguity Resolver};
    B -- Clarified Query --> C[Multi-Agent Orchestrator];
    C --> D1[Stage 1: Parallel Context Building];
    subgraph D1
        R[Retrieval Agent]
        S[Specialist Agent]
        V[Validator Agent]
    end
    D1 --> D2[Stage 2: Merge into UnifiedContext];
    D2 --> D3[Stage 3: Parallel Analysis];
    subgraph D3
        S1[Specialist 1: Gen SQL]
        S2[Specialist 2: Gen SQL]
        S3[Specialist 3: Gen SQL]
    end
    D3 --> D4{Stage 4: Bayesian Consensus Engine};
    D4 -- Winning SQL AST --> E[SQL Executor];
    E -- Raw Data --> F[Physics-Constrained Validator];
    F -- Validated Data --> G[Visualization Decision Engine];
    G --> H[Final Response: Text, Plots, Metadata];
    H --> A;

    subgraph Database
        TSDB[Unified Ocean Data Store <br> (PostgreSQL + TimescaleDB)];
        CD[Climatology Database <br> (World Ocean Atlas)];
    end

    E --> TSDB;
    F --> CD;
Technology Stack
Component	Technology
Backend	Python, FastAPI, asyncio
AI Models	OpenAI API (GPT-4-Turbo, GPT-3.5-Turbo), Model-Agnostic Design
NLP & Parsing	spaCy (for NER), sqlparse (for SQL AST)
Database	PostgreSQL (v14+), TimescaleDB, PostGIS
Data Processing	Pandas, NumPy, SciPy, xarray
Visualization	Plotly
Frontend	Streamlit
Deployment	Docker, Docker Compose
Getting Started
Prerequisites
Docker Desktop installed and running.
Python 3.11+
UV, an extremely fast Python package installer.
