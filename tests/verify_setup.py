#!/usr/bin/env python3
"""
Setup Verification Script for RAG PDF Chat Application
This script verifies that all components are properly installed and configured.
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_status(item, status, details=""):
    """Print status with emoji"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {item}")
    if details:
        print(f"   {details}")

def check_python_version():
    """Check Python version"""
    print_header("Python Environment Check")
    
    version = sys.version_info
    required_version = (3, 11)
    
    if version >= required_version:
        print_status(f"Python Version: {version.major}.{version.minor}.{version.micro}", True)
        return True
    else:
        print_status(f"Python Version: {version.major}.{version.minor}.{version.micro}", False, 
                    f"Required: {required_version[0]}.{required_version[1]}+")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print_header("Dependencies Check")
    
    required_packages = [
        'streamlit',
        'PyPDF2',
        'pdfplumber',
        'fitz',  # PyMuPDF
        'cv2',   # OpenCV
        'openai',
        'numpy',
        'sklearn',
        'sentence_transformers',
        'chromadb',
        'python-dotenv',
        'pandas',
        'pytesseract',
        'PIL'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'fitz':
                import fitz
                print_status("PyMuPDF (fitz)", True)
            elif package == 'cv2':
                import cv2
                print_status("OpenCV (cv2)", True)
            elif package == 'PIL':
                from PIL import Image
                print_status("Pillow (PIL)", True)
            else:
                importlib.import_module(package)
                print_status(package, True)
        except ImportError:
            print_status(package, False, "Not installed")
            all_installed = False
    
    return all_installed

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print_header("Tesseract OCR Check")
    
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_status("Tesseract OCR", True, version_line)
            return True
        else:
            print_status("Tesseract OCR", False, "Command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_status("Tesseract OCR", False, "Not found in PATH")
        return False

def check_environment():
    """Check environment configuration"""
    print_header("Environment Configuration Check")
    
    env_file = Path('.env')
    if env_file.exists():
        print_status(".env file", True)
        
        # Check for OpenAI API key
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content and 'your_openai_api_key_here' not in content:
                print_status("OpenAI API Key", True, "Configured")
                return True
            else:
                print_status("OpenAI API Key", False, "Not configured or using placeholder")
                return False
    else:
        print_status(".env file", False, "File not found")
        return False

def check_directories():
    """Check if required directories exist"""
    print_header("Directory Structure Check")
    
    required_dirs = ['uploads', 'embeddings', 'chroma_db']
    all_exist = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print_status(f"{directory}/", True)
        else:
            print_status(f"{directory}/", False, "Will be created automatically")
            all_exist = False
    
    return True  # Directories can be created automatically

def check_files():
    """Check if required files exist"""
    print_header("Required Files Check")
    
    required_files = [
        'app.py',
        'config.py',
        'pdf_uploader.py',
        'pdf_parser.py',
        'embedding_system.py',
        'rag_system.py',
        'run.py',
        'requirements.txt'
    ]
    
    all_exist = True
    
    for file in required_files:
        if Path(file).exists():
            print_status(file, True)
        else:
            print_status(file, False, "Missing required file")
            all_exist = False
    
    return all_exist

def check_docker():
    """Check Docker installation (optional)"""
    print_header("Docker Check (Optional)")
    
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_status("Docker", True, result.stdout.strip())
            
            # Check Docker Compose
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print_status("Docker Compose", True, result.stdout.strip())
                return True
            else:
                print_status("Docker Compose", False, "Not found")
                return False
        else:
            print_status("Docker", False, "Command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_status("Docker", False, "Not installed (optional for local development)")
        return False

def main():
    """Main verification function"""
    print("🚀 RAG PDF Chat Application - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Tesseract OCR", check_tesseract),
        ("Environment", check_environment),
        ("Directories", check_directories),
        ("Files", check_files),
        ("Docker (Optional)", check_docker)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("   1. Run: python run.py")
        print("   2. Or: streamlit run app.py")
        print("   3. Access: http://localhost:8501")
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please review the issues above.")
        print("\n🔧 Quick fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Install Tesseract OCR")
        print("   - Configure .env file with OpenAI API key")
        print("   - Run: python run.py (will create missing directories)")
    
    print(f"\n📚 For detailed setup instructions, see README.md")
    print(f"🌐 For portfolio integration, see PORTFOLIO_INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()
