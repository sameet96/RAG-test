#!/bin/bash

# Ollama Setup Script for RAG PDF Chat Application
# This script helps install and configure Ollama for Llama 3 models

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Setting up Ollama for RAG PDF Chat Application...${NC}"

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is already installed${NC}"
    ollama --version
else
    echo -e "${YELLOW}📦 Installing Ollama...${NC}"
    
    # Detect OS and install Ollama
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo -e "${YELLOW}Installing Ollama for macOS...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo -e "${YELLOW}Installing Ollama for Linux...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
        echo -e "${YELLOW}Please install Ollama manually from: https://ollama.ai/download${NC}"
        exit 1
    fi
fi

# Start Ollama service
echo -e "${YELLOW}🔄 Starting Ollama service...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - start Ollama in background
    ollama serve &
    sleep 3
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - start Ollama service
    sudo systemctl start ollama || ollama serve &
    sleep 3
fi

# Check if Ollama is running
echo -e "${YELLOW}🔍 Checking Ollama service...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo -e "${GREEN}✅ Ollama service is running${NC}"
else
    echo -e "${RED}❌ Ollama service is not running${NC}"
    echo -e "${YELLOW}Please start Ollama manually: ollama serve${NC}"
    exit 1
fi

# Pull Llama 3 models
echo -e "${YELLOW}📥 Pulling Llama 3 models...${NC}"

echo -e "${YELLOW}Pulling Llama 3 7B model...${NC}"
ollama pull llama3:7b

echo -e "${YELLOW}Pulling Llama 3 8B model...${NC}"
ollama pull llama3:8b

# List installed models
echo -e "${GREEN}📋 Installed models:${NC}"
ollama list

echo -e "${GREEN}🎉 Ollama setup complete!${NC}"
echo -e "${YELLOW}You can now use Llama 3 models in your RAG PDF Chat application.${NC}"

echo -e "\n${GREEN}📚 Next steps:${NC}"
echo -e "1. Run your application: ${YELLOW}python run.py${NC}"
echo -e "2. Select 'Llama 3 7B' or 'Llama 3 8B' from the model dropdown"
echo -e "3. Start chatting with your PDF documents!"

echo -e "\n${YELLOW}💡 Tips:${NC}"
echo -e "- Keep Ollama running in the background: ${YELLOW}ollama serve${NC}"
echo -e "- To stop Ollama: ${YELLOW}pkill ollama${NC}"
echo -e "- To see running models: ${YELLOW}ollama list${NC}"
echo -e "- To remove a model: ${YELLOW}ollama rm model_name${NC}"
