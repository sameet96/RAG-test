#!/bin/bash

# RAG PDF Chat Application Deployment Script
# Usage: ./deploy.sh [production|development]

set -e

MODE=${1:-development}
PROJECT_NAME="rag-pdf-chat"

echo "🚀 Deploying RAG PDF Chat Application in $MODE mode..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads embeddings chroma_db ssl

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
EOF
    echo "📝 Please update .env file with your OpenAI API key before running again."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if OpenAI API key is set
if [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Please set your OpenAI API key in the .env file"
    exit 1
fi

# Build and start services
echo "🔨 Building Docker image..."
docker-compose build

if [ "$MODE" = "production" ]; then
    echo "🚀 Starting production deployment with nginx..."
    docker-compose --profile production up -d
    echo "✅ Application deployed at http://localhost"
    echo "📊 RAG App accessible at http://localhost"
else
    echo "🚀 Starting development deployment..."
    docker-compose up -d rag-app
    echo "✅ Application deployed at http://localhost:8501"
fi

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "🎉 Deployment successful!"
    echo ""
    echo "📱 Access your RAG PDF Chat Application:"
    if [ "$MODE" = "production" ]; then
        echo "   🌐 http://localhost (with nginx)"
    else
        echo "   🌐 http://localhost:8501"
    fi
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop: docker-compose down"
    echo "   Restart: docker-compose restart"
    echo "   Update: ./deploy.sh $MODE"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi
