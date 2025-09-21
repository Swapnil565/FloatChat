#!/bin/bash
# 🌊 FloatChat Quick Setup Script
# Run this script to set up the complete FloatChat system

echo "🌊 FloatChat Ocean Analysis System Setup"
echo "========================================="

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop first."
    exit 1
fi
echo "✅ Docker found"

# Check UV
if ! command -v uv &> /dev/null; then
    echo "❌ UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi
echo "✅ UV found"

# Start database
echo "🐳 Starting PostgreSQL database..."
docker-compose up postgres -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Setup Python environment
echo "🐍 Setting up Python environment..."
uv venv floatchat-env

# Activate environment and install dependencies
echo "📦 Installing dependencies..."
source floatchat-env/bin/activate  # Linux/Mac
# For Windows: floatchat-env\Scripts\activate

uv pip install Flask psycopg2-binary pandas numpy requests python-dotenv scikit-learn plotly kaleido cerebras-cloud-sdk

# Test the system
echo "🧪 Testing FloatChat system..."
python test_docker_system.py

echo ""
echo "🎉 FloatChat setup complete!"
echo "========================================="
echo "🚀 To run the system:"
echo "   source floatchat-env/bin/activate  # Linux/Mac"
echo "   python lightweight_pipeline.py"
echo ""
echo "📊 Example query: 'show me the water profile of mumbai'"
echo "📁 Plots saved to: plots/"
echo ""
echo "🌊 Happy ocean data analysis! 🤿"