#!/bin/bash

echo "🚀 Setting up RAG Project Environment"
echo "======================================"

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "✅ Conda found! Creating environment from environment.yml..."
    conda env create -f environment.yml
    echo "✅ Environment 'rag-project' created successfully!"
    echo "To activate the environment, run: conda activate rag-project"
elif command -v python3 &> /dev/null; then
    echo "⚠️  Conda not found, creating virtual environment instead..."
    
    # Create virtual environment
    python3 -m venv rag-project-env
    echo "✅ Virtual environment created!"
    
    # Activate and install dependencies
    source rag-project-env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
    echo "To activate the environment, run: source rag-project-env/bin/activate"
else
    echo "❌ Neither conda nor python3 found. Please install Python first."
    exit 1
fi

echo "======================================"
echo "🎉 Setup complete!"
echo "Next steps:"
echo "1. Activate the environment"
echo "2. Create .env file with your OpenAI API key"
echo "3. Run: python run.py"
