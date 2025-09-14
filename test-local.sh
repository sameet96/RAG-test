#!/bin/bash

# Test script for local RAG application without Docker
echo "🧪 Testing RAG PDF Chat Application locally..."

# Check if virtual environment exists
if [ ! -d "rag-project-env" ]; then
    echo "❌ Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Activate virtual environment
source rag-project-env/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your OpenAI API key."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if OpenAI API key is set
if [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Please set your OpenAI API key in the .env file"
    exit 1
fi

echo "✅ Environment setup complete"
echo "🚀 Starting RAG PDF Chat Application..."
echo "📱 The app will be available at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

# Start the application
python run.py
