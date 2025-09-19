@echo off
echo 🔍 API Server Status Checker
echo ===========================

echo Checking if API server is running...
netstat -an | findstr :5000
if %ERRORLEVEL% == 0 (
    echo ✅ Something is running on port 5000
) else (
    echo ❌ Nothing running on port 5000
)

echo.
echo Checking API health...
curl -s http://localhost:5000/api/health
if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ API is responding
) else (
    echo ❌ API is not responding
)

echo.
echo To start the API server manually:
echo python production_api.py
echo.
pause
