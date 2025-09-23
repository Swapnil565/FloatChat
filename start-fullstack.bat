@echo off
REM 🌊 FloatChat Full Stack Startup Script for Windows
REM Runs both React frontend and Flask backend together

echo 🌊 Starting FloatChat Full Stack Application
echo =============================================

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: Run this script from the FloatChat project root directory
    exit /b 1
)

if not exist "api_server.py" (
    echo ❌ Error: Run this script from the FloatChat project root directory
    exit /b 1
)

REM Check if database is running
echo 🐳 Checking database connection...
docker ps | findstr "floatchat-postgres" >nul
if %errorlevel% neq 0 (
    echo 🚀 Starting PostgreSQL database...
    docker-compose up postgres -d
    echo ⏳ Waiting for database to be ready...
    timeout /t 10 /nobreak >nul
)

REM Activate Python environment if it exists
if exist "floatchat-env\Scripts\activate.bat" (
    echo 🐍 Activating Python virtual environment...
    call floatchat-env\Scripts\activate.bat
)

REM Install Node.js dependencies if needed
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
)

REM Check Python dependencies
echo 🔧 Checking Python dependencies...
python -c "import flask, pandas, plotly" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
)

REM Create plots directory if it doesn't exist
if not exist "plots" mkdir plots

echo.
echo 🚀 Starting FloatChat services...
echo ==================================

REM Start Flask API server in background
echo 🔥 Starting Flask API server on http://localhost:5000...
start /b python api_server.py

REM Wait a moment for API to start
timeout /t 3 /nobreak >nul

REM Start React development server
echo ⚛️  Starting React frontend on http://localhost:3000...
set BROWSER=none
start /b npm start

REM Wait for services to start
timeout /t 5 /nobreak >nul

echo.
echo 🎉 FloatChat Full Stack Application Started!
echo =============================================
echo 🌐 Frontend (React):   http://localhost:3000
echo 🔌 Backend API (Flask): http://localhost:5000
echo 🗄️  Database (PostgreSQL): localhost:5432
echo.
echo 📊 Try these queries:
echo    • 'show me the water profile of mumbai'
echo    • 'temperature trends in indian ocean'
echo    • 'warm water near mumbai'
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Press Ctrl+C to stop all services when you're done
pause