@echo off
echo 🚀 Career Guidance System - Windows Installer
echo =============================================

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Python found!
    python --version
) else (
    echo ❌ Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo ⚠️ IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing required packages...
pip install pandas numpy scikit-learn flask flask-cors
if %ERRORLEVEL% neq 0 (
    echo ❌ Package installation failed!
    echo Try running as Administrator or check internet connection.
    pause
    exit /b 1
)

echo.
echo Step 3: Setting up database...
python setup_database.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Database setup failed!
    pause
    exit /b 1
)

echo.
echo Step 4: Loading college data...
python data_manager.py --update data/jk_colleges_clean.csv
if %ERRORLEVEL% neq 0 (
    echo ⚠️ College data loading had issues, but continuing...
)

echo.
echo Step 5: Starting the system...
echo ✅ Career Guidance System is starting!
echo.
echo 🌐 API will be available at: http://localhost:5000
echo 🌐 Open frontend/index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.
python production_api.py
