#!/usr/bin/env python3
"""
Startup script for the RAG PDF Chat Application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import fitz
        import pdfplumber
        import openai
        import chromadb
        import sentence_transformers
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Tesseract OCR not found")
    print("Please install Tesseract:")
    print("  macOS: brew install tesseract")
    print("  Ubuntu: sudo apt-get install tesseract-ocr")
    print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Please create a .env file with your OpenAI API key:")
        print("  OPENAI_API_KEY=your_api_key_here")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "embeddings"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def main():
    """Main startup function"""
    print("🚀 Starting RAG PDF Chat Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Tesseract
    if not check_tesseract():
        print("⚠️  OCR functionality will not work without Tesseract")
    
    # Check environment file
    check_env_file()
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("🎉 Setup complete! Starting the application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("=" * 50)
    
    # Start Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
