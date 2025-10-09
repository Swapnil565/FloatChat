<h1 align="center">🌊 FloatChat: Conversational AI for Ocean Data Exploration</h1>

<p align="center">
  <b>Multi-Agent Conversational AI that understands, validates & explains oceanographic data — scientifically.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
</p>

---

### 🧠 Imagine This
Ask:
> “Show me temperature anomalies west of the Andaman Islands for last month.”

Get:
- A **validated, multi-layered ocean analysis**
- Interactive charts, metadata, and explanations — all **within seconds**  

<!-- Optional: Add a GIF demo -->
![Demo Placeholder](https://user-images.githubusercontent.com/12345/67890.gif)

---

## 🚀 The FloatChat Difference

### 🧩 Multi-Agent Cognitive Architecture
A team of specialized AI agents (**Retriever**, **SQL Generator**, **Validator**) collaborate like a research group.  
They build context, generate multiple hypotheses, and reach consensus using a **Bayesian Consensus Engine**.

### 🌍 Physics-Constrained AI Validation
Every output is **cross-checked** against climatological datasets (e.g., **World Ocean Atlas**) to ensure all results are **scientifically plausible** — not hallucinations.

### ⚡ Smart & Cost-Efficient Text-to-SQL
- 80% of queries handled via **pre-tuned SQL templates** (millisecond response)
- Novel queries fallback to **GPT-4** safely
- **EXPLAIN-based cost guardrail** prevents expensive or malicious queries

### 💬 Natural Conversational UX
Handles vague queries like _“warm water near Mumbai”_ using **Ambiguity Resolver**:
- Sets defaults (e.g., warm > 28 °C, near = 100 km)
- Offers **sliders & interactive controls** to refine results — no re-typing required

### 🧠 Enterprise-Grade Data Backend
Powered by:
- **PostgreSQL + TimescaleDB + PostGIS**
- Unified architecture for petabyte-scale **time-series + geospatial** data

---

## 🧱 System Architecture

```mermaid
graph TD
    A[User Query via Streamlit UI] --> B{Ambiguity Resolver}
    B --> C[Multi-Agent Orchestrator]
    C --> D1[Stage 1: Context Building]
    subgraph D1
        R[Retrieval Agent]
        S[Specialist Agent]
        V[Validator Agent]
    end
    D1 --> D2[Stage 2: Merge Context]
    D2 --> D3[Stage 3: SQL Generation]
    subgraph D3
        S1[SQL Specialist 1]
        S2[SQL Specialist 2]
        S3[SQL Specialist 3]
    end
    D3 --> D4{Stage 4: Consensus Engine}
    D4 --> E[SQL Executor]
    E --> F[Physics Validator]
    F --> G[Visualization Engine]
    G --> H[Final Response]
    H --> A

    subgraph Database
        TSDB[Ocean Data Store]
        CD[Climatology Data]
    end

    E --> TSDB
    F --> CD


🧰 Technology Stack
Component	Technology
Backend	Python, FastAPI, asyncio
AI Models	OpenAI GPT-4-Turbo / GPT-3.5-Turbo (model-agnostic)
NLP & Parsing	spaCy, sqlparse
Database	PostgreSQL 14+, TimescaleDB, PostGIS
Data Processing	Pandas, NumPy, SciPy, xarray
Visualization	Plotly
Frontend	Streamlit
Deployment	Docker, Docker Compose

<details> <summary><b>🧭 Getting Started (click to expand)</b></summary>
✅ Prerequisites
Docker Desktop installed & running

Python 3.11 or newer

UV (ultra-fast Python package installer)

1️⃣ Launch the Database
bash
Copy code
docker-compose up postgres -d
Check status:

bash
Copy code
docker ps
2️⃣ Setup Python Environment
bash
Copy code
# Create a virtual environment
uv venv

# Activate it
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
3️⃣ Configure Environment Variables
Create .env in project root:

env
Copy code
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=floatchat_ocean_data
DB_USER=floatchat_user
DB_PASSWORD=your_secure_password

# AI Provider
OPENAI_API_KEY=your_api_key_here
4️⃣ Run FloatChat
bash
Copy code
# Run system test
python test_docker_system.py

# OR start app
streamlit run app.py
Then open 👉 http://localhost:8501

</details>
🤝 Contributing
We ❤️ contributions!
Check CONTRIBUTING.md for:

🪶 Issue creation

🔀 Pull requests

🧭 Coding standards

🧾 License
Licensed under MIT License.
See LICENSE for details.

🌍 Acknowledgments
🌊 ARGO Program — global ocean observation data

🐘 PostgreSQL, 🕒 TimescaleDB, 📍 PostGIS — world-class open-source data tech

💡 Open-source community for tools like Plotly, spaCy, Streamlit

<p align="center"> <i>“Bridging AI and Ocean Science — One Conversation at a Time.”</i> <br>🌊 <b>FloatChat</b> © 2025 </p> ```
