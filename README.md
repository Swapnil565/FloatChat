# 🌊 FloatChat - Ocean Data Analysis System

**AI-Powered Ocean Data Query System with Real-Time Visualization**

FloatChat is an intelligent ocean data analysis system that processes ARGO float data to provide comprehensive oceanographic insights through natural language queries. The system generates multiple complementary visualizations and scientific analysis using a lightweight ML pipeline.

## 🚀 Quick Start with Docker + UV

### Prerequisites
- Docker Desktop installed and running
- Python 3.11+ with `uv` package manager
- Git for version control

### 🐳 1. Start Database Container
```bash
# Start PostgreSQL with PostGIS (contains 54,703 ARGO records)
docker-compose up postgres -d

# Verify database is running
docker ps
```

### ⚡ 2. Setup Python Environment with UV
```bash
# Create virtual environment
uv venv floatchat-env

# Activate environment (Windows)
floatchat-env\Scripts\activate

# Install dependencies
uv pip install Flask psycopg2-binary pandas numpy requests python-dotenv scikit-learn plotly kaleido cerebras-cloud-sdk
```

### 🌊 3. Run FloatChat System
```bash
# Test the complete system
python test_docker_system.py

# Or run directly
python lightweight_pipeline.py
```

## 🎯 Example Usage

**Query:** `"show me the water profile of mumbai"`

**System Response:**
- 🔍 Analyzes 5,000 ocean measurements
- 🎨 Generates 4 complementary plots automatically
- 📊 Provides scientific oceanographic analysis
- 💾 Saves PNG diagrams with timestamps

**Generated Plots:**
1. **Temperature Profile** - Vertical temperature distribution
2. **Salinity Profile** - Vertical salinity distribution  
3. **T-S Diagram** - Temperature-Salinity relationship
4. **3D Ocean Scatter** - Interactive 3D visualization

## 🏗️ System Architecture

### Core Components
- **`lightweight_pipeline.py`** - Main system orchestrator
- **`lightweight_plot_generator.py`** - Intelligent multi-plot generation
- **`sql_query_generator.py`** - Spatial database queries
- **`floatchat_bot.py`** - AI response generation

### Database
- **PostgreSQL + PostGIS** - Spatial ocean data storage
- **54,703 ARGO Records** - Real ocean measurements
- **Spatial Indexing** - Optimized geographic queries

### ML Pipeline
- **scikit-learn** - Lightweight classification (230MB+ size reduction vs torch)
- **Intelligent Plot Selection** - Rule-based + ML scoring
- **Multi-Plot Generation** - Automatically creates complementary visualizations

## 📊 Features

### 🧠 Intelligent Analysis
- **Natural Language Processing** - Query intent classification
- **Spatial Queries** - Geographic ocean data filtering
- **Multi-Plot Intelligence** - Generates 4+ complementary visualizations
- **Scientific Context** - Oceanographic analysis and interpretation

### 🎨 Visualization Types
- **Profile Plots** - Vertical ocean property distributions
- **Geographic Maps** - Spatial temperature/salinity patterns
- **T-S Diagrams** - Water mass identification
- **3D Scatter** - Interactive depth-temperature-salinity views
- **Time Series** - Temporal ocean changes

### ⚡ Performance
- **Lightweight** - scikit-learn instead of torch/transformers
- **Fast Setup** - UV package manager for rapid installation
- **Docker Ready** - Containerized PostgreSQL database
- **PNG Export** - High-quality 1200x800 visualizations

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=floatchat_ocean_data
DB_USER=floatchat_user
DB_PASSWORD=your_secure_password

# Cerebras AI API
CEREBRAS_API_KEY=your_api_key_here

# Optional: Redis Cache
REDIS_URL=redis://localhost:6379
```

### Docker Configuration
The system uses `docker-compose.yml` with:
- PostgreSQL 15 + PostGIS 3.3
- Persistent data volumes
- Health checks
- Network isolation

## 📁 Project Structure

```
FloatChat/
├── 🐳 Docker Setup
│   ├── docker-compose.yml      # Container orchestration
│   ├── Dockerfile             # Application container
│   └── .env.docker           # Docker environment
├── 🧠 Core System
│   ├── lightweight_pipeline.py       # Main orchestrator
│   ├── lightweight_plot_generator.py # Intelligent plotting
│   ├── sql_query_generator.py       # Database queries
│   └── floatchat_bot.py             # AI responses
├── 🧪 Testing
│   └── test_docker_system.py   # System integration tests
├── 📚 Documentation
│   ├── README_Docker.md        # Docker setup guide
│   └── DOCKER_COMMANDS.md      # Docker reference
└── 📊 Output
    └── plots/                  # Generated PNG visualizations
```

## 🧪 Testing

### System Health Check
```bash
python test_docker_system.py
```

**Expected Output:**
```
🚀 FloatChat Docker System Test
✅ PostgreSQL container is running
✅ Database connected: 54,703 records available
✅ Spatial queries working
✅ FloatChat pipeline functioning
🎯 Test Results: 3/3 tests passed
```

### Manual Testing
```bash
# Direct pipeline test
python lightweight_pipeline.py

# Check database connection
docker exec floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data -c "SELECT COUNT(*) FROM argo_floats;"
```

## 🌊 Ocean Data

### ARGO Float Dataset
- **54,703 measurements** from global ocean floats
- **Geographic Coverage** - Global ocean basins
- **Depth Range** - Surface to 2000+ meters
- **Parameters** - Temperature, Salinity, Pressure, Location
- **Spatial Indexing** - PostGIS geometry for fast queries

### Data Schema
```sql
Table: argo_floats
├── float_id (text)           # Unique float identifier
├── profile_number (integer)  # Profile sequence number
├── cycle_number (integer)    # Measurement cycle
├── latitude (real)           # Geographic latitude
├── longitude (real)          # Geographic longitude
├── date_time (timestamp)     # Measurement timestamp
├── level (integer)           # Depth level index
├── pressure_dbar (real)      # Ocean pressure (decibars)
├── temperature_celsius (real) # Water temperature (°C)
├── salinity_psu (real)       # Salinity (PSU)
└── geometry (geometry)       # PostGIS spatial column
```

## 🚀 Deployment Options

### 1. Local Development (Recommended)
```bash
# Start database
docker-compose up postgres -d

# Run with UV
uv venv floatchat-env && floatchat-env\Scripts\activate
uv pip install -r requirements.txt
python lightweight_pipeline.py
```

### 2. Full Docker Stack
```bash
# Build and run everything
docker-compose up --build -d

# Check logs
docker-compose logs -f
```

### 3. Production Deployment
- Use `gunicorn` for WSGI serving
- Configure nginx reverse proxy
- Set up SSL certificates
- Use managed PostgreSQL service
- Implement Redis caching

## 🔬 Scientific Applications

### Oceanographic Research
- **Water Mass Analysis** - T-S diagram classification
- **Thermocline Detection** - Vertical temperature gradients
- **Regional Oceanography** - Spatial pattern analysis
- **Climate Studies** - Long-term ocean trends

### Educational Use
- **Ocean Science Teaching** - Interactive visualizations
- **Data Science Training** - Real-world spatial datasets
- **Marine Biology** - Environmental context for ecosystems
- **Climate Education** - Ocean-atmosphere interactions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `uv pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest tests/`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open Pull Request

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Document functions with docstrings
- Add tests for new features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ARGO Program** - Global ocean observation data
- **PostGIS** - Spatial database capabilities
- **Plotly** - Interactive visualization library
- **scikit-learn** - Machine learning framework
- **Cerebras** - AI language model API

## 📧 Contact

**Swapnil565** - [GitHub Profile](https://github.com/Swapnil565)

**Project Link:** https://github.com/Swapnil565/FloatChat

---

*🌊 Dive deep into ocean data with FloatChat! 🤿*