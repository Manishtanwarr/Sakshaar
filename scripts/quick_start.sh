#!/bin/bash
echo "🚀 Career Guidance System - Quick Start"
echo "======================================"

# Check if Docker is available
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker found - Starting with containers..."
    docker-compose up -d
    echo "🌐 System starting at http://localhost"
    echo "📊 API available at http://localhost:5000"
else
    echo "⚠ Docker not found - Using Python setup..."

    # Check Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python found - Installing dependencies..."
        pip3 install -r requirements_production.txt

        echo "📊 Setting up database..."
        python3 setup_database.py

        echo "📈 Loading college data..."
        python3 data_manager.py --update data/jk_colleges_clean.csv

        echo "🚀 Starting API server..."
        python3 production_api.py &

        echo "🌐 Open frontend/index.html in your browser"
        echo "📊 API running at http://localhost:5000"
    else
        echo "❌ Python not found. Please install Python 3.8+ and try again."
    fi
fi
