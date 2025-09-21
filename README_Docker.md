# FloatChat - Dockerized Ocean Data Analysis System

🌊 **Complete ocean data analysis with real ARGO float data, Docker containerization, and lightweight ML pipeline**

## 🚀 Quick Start (Docker Setup)

### Prerequisites
- Docker Desktop installed and running
- Python 3.8+ installed
- Git installed

### 1. Clone and Setup
```bash
git clone <your-repo>
cd Floatchat_SIH

# Create Python virtual environment
python -m venv Floatchat_SIH
source Floatchat_SIH/bin/activate  # Linux/Mac
# OR
Floatchat_SIH\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Start Docker Services
```bash
# Start PostgreSQL database with real ocean data
docker-compose up -d

# Wait 30 seconds for database initialization
# The container will automatically load 54,703 ARGO float records
```

### 3. Verify System
```bash
# Run system test
python test_docker_system.py

# Expected output:
# ✅ PostgreSQL container is running
# ✅ Database connected: 54,703 records available
# ✅ Spatial queries working: 1000 records near Mumbai
# ✅ Pipeline initialized successfully
# ✅ Pipeline test successful
# 🎉 ALL TESTS PASSED!
```

### 4. Start Using FloatChat
```bash
# Run the main system
python lightweight_pipeline.py

# Or use interactive mode
python -c "
from lightweight_pipeline import LightweightFloatChatPipeline
pipeline = LightweightFloatChatPipeline()
response = pipeline.process_query('show me water profile of mumbai')
print(response['chat_response'])
"
```

## 🌊 What You Get

### Real Ocean Data
- **54,703 real ARGO float measurements**
- Temperature, salinity, pressure profiles
- Global coverage with focus on Indian Ocean
- Spatial queries using PostGIS

### Lightweight ML Pipeline
- **No torch dependency** (230MB+ saved)
- scikit-learn for plot classification
- Same performance as original system
- Fast initialization and queries

### Docker Containerization
- PostgreSQL + PostGIS database
- Persistent data volumes
- Production-ready configuration
- Easy deployment to any machine

## 🔧 System Architecture

```
FloatChat System
├── Docker Services
│   ├── PostgreSQL + PostGIS (port 5432)
│   └── Real ARGO data (54,703 records)
├── Python Pipeline
│   ├── SQL Query Generator
│   ├── Spatial Database Queries
│   ├── 3D Plot Generation
│   └── AI-Powered Responses
└── Lightweight ML
    ├── scikit-learn classifier
    ├── Plot type detection
    └── Data visualization
```

## 📊 Example Queries

Try these sample queries:

```python
# Mumbai water analysis
"show me water profile of mumbai"

# Temperature analysis
"temperature patterns in arabian sea"

# 3D visualization
"3d plot of ocean data near india"

# Regional analysis
"bay of bengal salinity profile"
```

## 🗂️ Project Structure

```
Floatchat_SIH/
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Application container
├── init_db.sql                # Database initialization
├── requirements.txt           # Python dependencies
├── lightweight_pipeline.py    # Main pipeline (no torch)
├── lightweight_plot_generator.py # Plotting with scikit-learn
├── sql_query_generator.py     # Spatial SQL generation
├── floatchat_bot.py           # AI response generation
├── test_docker_system.py      # System verification
└── data/
    └── ARGO_float_data.csv    # Real ocean measurements
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Check status
docker ps

# View logs
docker-compose logs floatchat-postgres

# Stop services
docker-compose down

# Restart database
docker-compose restart floatchat-postgres

# Access database directly
docker exec -it floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data
```

## 🔍 Database Schema

```sql
-- ARGO floats table
CREATE TABLE argo_floats (
    float_id VARCHAR(20),
    profile_number INTEGER,
    cycle_number INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    date_time TIMESTAMP,
    level INTEGER,
    pressure_dbar DOUBLE PRECISION,
    temperature_celsius DOUBLE PRECISION,
    salinity_psu DOUBLE PRECISION,
    geometry GEOMETRY(POINT, 4326)  -- PostGIS spatial column
);

-- Spatial index for fast queries
CREATE INDEX idx_argo_floats_geometry ON argo_floats USING GIST (geometry);
```

## 🌍 Deployment to Other Machines

### Option 1: Docker Hub (Recommended)
```bash
# Build and push image
docker build -t your-username/floatchat .
docker push your-username/floatchat

# On other machine
docker pull your-username/floatchat
docker-compose up -d
```

### Option 2: Local Transfer
```bash
# Export images
docker save postgis/postgis:15-3.3 > floatchat-postgres.tar

# Transfer files to other machine
scp -r Floatchat_SIH/ user@other-machine:/path/

# On other machine
docker load < floatchat-postgres.tar
docker-compose up -d
```

### Option 3: Git Repository
```bash
# On other machine
git clone <your-repo>
cd Floatchat_SIH
docker-compose up -d
python test_docker_system.py
```

## 🚀 Performance Features

- **Fast Startup**: No torch loading (5x faster initialization)
- **Small Footprint**: 230MB+ smaller than torch version
- **Real Data**: 54,703 actual ocean measurements
- **Spatial Queries**: PostGIS for geographic analysis
- **3D Visualization**: Interactive plots with plotly
- **AI Responses**: Context-aware oceanographic analysis

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check container status
docker ps

# Restart database
docker-compose restart floatchat-postgres

# View logs
docker-compose logs floatchat-postgres
```

### Python Environment Issues
```bash
# Recreate virtual environment
rm -rf Floatchat_SIH/
python -m venv Floatchat_SIH
source Floatchat_SIH/bin/activate
pip install -r requirements.txt
```

### Data Loading Issues
```bash
# Check data file exists
ls -la data/ARGO_float_data.csv

# Manually reload data
docker exec -it floatchat-postgres psql -U floatchat_user -d floatchat_ocean_data -c "SELECT COUNT(*) FROM argo_floats;"
```

## 📈 System Requirements

- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB for Docker images + data
- **CPU**: Any modern processor (optimized for efficiency)
- **Network**: Internet for AI responses (Cerebras API)

## 🎯 Next Steps

1. **Customize Queries**: Modify `sql_query_generator.py` for specific regions
2. **Add Plot Types**: Extend `lightweight_plot_generator.py` with new visualizations
3. **Scale Database**: Add more ARGO data or other ocean datasets
4. **API Integration**: Create REST API for web applications
5. **Advanced Analytics**: Add machine learning models for prediction

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**🌊 FloatChat: Making ocean data analysis accessible to everyone!**