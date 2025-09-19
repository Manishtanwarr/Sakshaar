
import sys
import subprocess
import pkg_resources

def check_python_version():
    print("🐍 PYTHON VERSION CHECK")
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    if sys.version_info >= (3, 8):
        print("✅ Python version is compatible!")
        return True
    else:
        print("❌ Python 3.8+ required. Please upgrade.")
        return False

def check_required_packages():
    print("\n📦 CHECKING REQUIRED PACKAGES")
    print("=" * 40)

    required = ['pandas', 'numpy', 'scikit-learn', 'flask', 'flask-cors']
    missing = []

    for package in required:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package}: Installed")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: Missing")
            missing.append(package)

    if missing:
        print(f"\n🔧 To install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    else:
        print("\n🎉 All required packages are installed!")
        return True

def main():
    print("🚀 CAREER GUIDANCE SYSTEM - ENVIRONMENT CHECK")
    print("=" * 50)

    python_ok = check_python_version()
    if not python_ok:
        return

    packages_ok = check_required_packages()

    if python_ok and packages_ok:
        print("\n✅ SYSTEM READY!")
        print("Next steps:")
        print("1. python setup_database.py")
        print("2. python data_manager.py --update data/jk_colleges_clean.csv")
        print("3. python production_api.py")
        print("4. Open frontend/index.html in browser")
    else:
        print("\n⚠️ Please fix the issues above and try again.")

if __name__ == "__main__":
    main()
