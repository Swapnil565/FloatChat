#!/bin/bash
# 🌊 FloatChat Full Stack Startup Script
# Runs both React frontend and Flask backend together

echo "🌊 Starting FloatChat Full Stack Application"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "api_server.py" ]; then
    echo "❌ Error: Run this script from the FloatChat project root directory"
    exit 1
fi

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check required ports
echo "🔍 Checking available ports..."
if ! check_port 3000; then
    echo "❌ React development server port (3000) is busy"
    exit 1
fi

if ! check_port 5000; then
    echo "❌ Flask API server port (5000) is busy"
    exit 1
fi

# Check if database is running
echo "🐳 Checking database connection..."
if ! docker ps | grep -q "floatchat-postgres"; then
    echo "🚀 Starting PostgreSQL database..."
    docker-compose up postgres -d
    echo "⏳ Waiting for database to be ready..."
    sleep 10
fi

# Activate Python environment if it exists
if [ -d "floatchat-env" ]; then
    echo "🐍 Activating Python virtual environment..."
    source floatchat-env/bin/activate
fi

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check Python dependencies
echo "🔧 Checking Python dependencies..."
python -c "import flask, pandas, plotly" 2>/dev/null || {
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
}

# Create plots directory if it doesn't exist
mkdir -p plots

echo ""
echo "🚀 Starting FloatChat services..."
echo "=================================="

# Start Flask API server in background
echo "🔥 Starting Flask API server on http://localhost:5000..."
python api_server.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Start React development server
echo "⚛️  Starting React frontend on http://localhost:3000..."
BROWSER=none npm start &
FRONTEND_PID=$!

# Wait for services to start
sleep 5

echo ""
echo "🎉 FloatChat Full Stack Application Started!"
echo "============================================="
echo "🌐 Frontend (React):   http://localhost:3000"
echo "🔌 Backend API (Flask): http://localhost:5000"
echo "🗄️  Database (PostgreSQL): localhost:5432"
echo ""
echo "📊 Try these queries:"
echo "   • 'show me the water profile of mumbai'"
echo "   • 'temperature trends in indian ocean'"
echo "   • 'warm water near mumbai'"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down FloatChat services..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup INT TERM

# Wait for user to stop the script
wait