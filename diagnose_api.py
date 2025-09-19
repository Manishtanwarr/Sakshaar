#!/usr/bin/env python3
"""
API Server Diagnostic Script
Career Guidance System
"""

import os
import sys
import subprocess
import socket
import time
import requests

def check_python_environment():
    print("🐍 PYTHON ENVIRONMENT CHECK")
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")

    required_modules = ['flask', 'flask_cors', 'pandas', 'numpy', 'sklearn']
    missing = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
        except ImportError:
            print(f"❌ {module}: Missing")
            missing.append(module)

    return len(missing) == 0

def check_port_availability():
    print("\n🌐 PORT AVAILABILITY CHECK")
    print("=" * 40)

    try:
        # Check if port 5000 is in use
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()

        if result == 0:
            print("⚠️  Port 5000 is already in use")
            return False
        else:
            print("✅ Port 5000 is available")
            return True
    except Exception as e:
        print(f"❌ Port check failed: {e}")
        return False

def check_required_files():
    print("\n📁 REQUIRED FILES CHECK")
    print("=" * 40)

    required_files = [
        'production_api.py',
        'setup_database.py', 
        'data_manager.py',
        'data/jk_colleges_clean.csv'
    ]

    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing")
            all_present = False

    return all_present

def check_database():
    print("\n🗄️  DATABASE CHECK")
    print("=" * 40)

    if os.path.exists('career_guidance.db'):
        print("✅ Database file exists")

        # Try to connect to database
        try:
            import sqlite3
            conn = sqlite3.connect('career_guidance.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM colleges')
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ Database connection successful: {count} colleges")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    else:
        print("❌ Database file not found")
        return False

def test_api_startup():
    print("\n🚀 API STARTUP TEST")
    print("=" * 40)

    try:
        print("Attempting to start API server (will timeout in 10 seconds)...")

        # Try to import the production API
        sys.path.insert(0, os.getcwd())
        import production_api
        print("✅ API module imported successfully")

        # The actual server start would block, so we just test the import
        return True

    except Exception as e:
        print(f"❌ API startup failed: {e}")
        return False

def test_api_connection():
    print("\n🔗 API CONNECTION TEST")
    print("=" * 40)

    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ API is responding")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"⚠️  API responding with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API not responding (connection refused)")
        return False
    except requests.exceptions.Timeout:
        print("❌ API not responding (timeout)")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    print("🔧 CAREER GUIDANCE SYSTEM - API DIAGNOSTIC")
    print("=" * 50)

    checks = [
        ("Python Environment", check_python_environment),
        ("Port Availability", check_port_availability), 
        ("Required Files", check_required_files),
        ("Database", check_database),
        ("API Module", test_api_startup),
        ("API Connection", test_api_connection)
    ]

    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check crashed: {e}")
            results.append((check_name, False))

    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)

    all_good = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:20} {status}")
        if not result:
            all_good = False

    print("\n🎯 RECOMMENDATIONS")
    print("=" * 50)

    if not results[0][1]:  # Python environment
        print("1. Install missing Python packages:")
        print("   pip install flask flask-cors pandas numpy scikit-learn")

    if not results[1][1]:  # Port availability  
        print("2. Port 5000 is busy. Kill the process or use different port")
        print("   netstat -ano | findstr :5000")

    if not results[2][1]:  # Required files
        print("3. Missing required files. Check project structure.")

    if not results[3][1]:  # Database
        print("4. Database issue. Run: python setup_database.py")
        print("   Then: python data_manager.py --update data/jk_colleges_clean.csv")

    if not results[4][1]:  # API module
        print("5. API module issue. Check production_api.py for errors.")

    if not results[5][1]:  # API connection
        print("6. API server not running. Start with: python production_api.py")

    if all_good:
        print("✅ All checks passed! System should be working.")
    else:
        print("⚠️  Issues found. Follow recommendations above.")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
