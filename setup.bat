@echo off
REM 🌊 FloatChat Quick Setup Script for Windows
REM Run this script to set up the complete FloatChat system

echo 🌊 FloatChat Ocean Analysis System Setup
echo =========================================

REM Check prerequisites
echo 🔍 Checking prerequisites...

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker Desktop first.
    exit /b 1
)
echo ✅ Docker found

REM Check UV
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ UV not found. Please install UV first: https://docs.astral.sh/uv/getting-started/installation/
    exit /b 1
)
echo ✅ UV found

REM Start database
echo 🐳 Starting PostgreSQL database...
docker-compose up postgres -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Setup Python environment
echo 🐍 Setting up Python environment...
uv venv floatchat-env

REM Activate environment and install dependencies
echo 📦 Installing dependencies...
call floatchat-env\Scripts\activate
uv pip install Flask psycopg2-binary pandas numpy requests python-dotenv scikit-learn plotly kaleido cerebras-cloud-sdk

REM Test the system
echo 🧪 Testing FloatChat system...
python test_docker_system.py

echo.
echo 🎉 FloatChat setup complete!
echo =========================================
echo 🚀 To run the system:
echo    floatchat-env\Scripts\activate
echo    python lightweight_pipeline.py
echo.
echo 📊 Example query: 'show me the water profile of mumbai'
echo 📁 Plots saved to: plots/
echo.
echo 🌊 Happy ocean data analysis! 🤿

pause