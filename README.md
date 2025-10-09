FloatChat: A Conversational AI Platform for Ocean Data Exploration
FloatChat is a sophisticated, multi-agent AI system designed to unlock insights from complex oceanographic data through natural language. It moves beyond simple Text-to-SQL, acting as a cognitive partner that can reason, validate, and explain scientific findings, ensuring every answer is not just fast, but also scientifically sound and trustworthy.
![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

![alt text](https://img.shields.io/badge/python-3.11+-blue.svg)

![alt text](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![alt text](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
Imagine asking complex questions about the ocean—"Show me temperature anomalies west of the Andaman Islands for last month"—and receiving not just a chart, but a validated, multi-faceted analysis in seconds. That is the power of FloatChat.
<!-- Recommended: Add a GIF of the application in action here -->
![alt text](https://user-images.githubusercontent.com/12345/67890.gif)

(Placeholder for a demo GIF)
The FloatChat Difference: Core Features
FloatChat is built on a foundation of cutting-edge architectural principles that differentiate it from standard data chatbot projects.
Multi-Agent Cognitive Architecture
Instead of a single, monolithic LLM, FloatChat employs a team of specialized AI agents that collaborate to understand, analyze, and respond to your query. This system mimics a human research team, with agents for retrieval, SQL generation, and validation working in parallel to reach a consensus on the best answer. This makes the system more robust, accurate, and resilient to single-agent failure.
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
1. Launch the Database
The docker-compose.yml file will start a PostgreSQL container with the TimescaleDB & PostGIS extensions, pre-loaded with over 54,000 ARGO float records.
code
Bash
docker-compose up postgres -d
Wait a moment for the database to initialize. You can check its status with docker ps.
2. Set Up the Python Environment
We use uv for a fast and reliable setup.
code
Bash
# Create a virtual environment
uv venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies from requirements.txt
uv pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory and add your credentials.
code
Env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=floatchat_ocean_data
DB_USER=floatchat_user
DB_PASSWORD=your_secure_password

# OpenAI API Key (or other AI provider)
OPENAI_API_KEY=your_api_key_here
4. Run FloatChat
You can run the system integration test to verify everything is working, or launch the main application directly.
code
Bash
# Run the integration test
python test_docker_system.py

# --- OR ---

# Launch the Streamlit application
streamlit run app.py
Now, open your browser to the URL provided by Streamlit (usually http://localhost:8501) to start interacting with FloatChat.
Contributing
We welcome contributions to make FloatChat even better. Please see our CONTRIBUTING.md file for guidelines on how to submit issues, fork the repository, and create pull requests.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments
The ARGO Program for providing the crucial global ocean observation data.
The development teams behind PostgreSQL, TimescaleDB, and PostGIS for creating an incredible open-source data platform.
The open-source community for libraries like Plotly, spaCy, and Streamlit.
