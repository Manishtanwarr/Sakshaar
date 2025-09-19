@echo off
echo 🚀 Career Guidance System - Quick Start
echo ======================================

REM Check if Docker is available
docker --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Docker found - Starting with containers...
    docker-compose up -d
    echo 🌐 System starting at http://localhost
    echo 📊 API available at http://localhost:5000
) else (
    echo ⚠ Docker not found - Using Python setup...

    REM Check Python
    python --version >nul 2>&1
    if %ERRORLEVEL% == 0 (
        echo ✅ Python found - Installing dependencies...
        pip install -r requirements_production.txt

        echo 📊 Setting up database...
        python setup_database.py

        echo 📈 Loading college data...
        python data_manager.py --update data/jk_colleges_clean.csv

        echo 🚀 Starting API server...
        start python production_api.py

        echo 🌐 Open frontend/index.html in your browser
        echo 📊 API running at http://localhost:5000
    ) else (
        echo ❌ Python not found. Please install Python 3.8+ and try again.
    )
)
pause
