# RAG PDF Chat Application

A sophisticated multi-model RAG (Retrieval-Augmented Generation) system for PDF document chat, supporting both OpenAI GPT models and Llama 3 via Ollama.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## 📁 Project Structure

```
RAG-test/
├── src/                    # Source code
│   ├── app.py             # Main Streamlit application
│   ├── core/              # Core functionality
│   │   ├── rag_system.py
│   │   ├── model_manager.py
│   │   ├── embedding_system.py
│   │   └── pdf_parser.py
│   ├── utils/             # Utility functions
│   │   └── pdf_uploader.py
│   └── config/            # Configuration
│       └── config.py
├── config/                # Configuration files
├── docs/                  # Documentation
├── scripts/               # Scripts and tools
├── tests/                 # Test files
├── docker/                # Docker files
├── data/                  # Data directories
│   ├── uploads/           # Uploaded PDFs
│   └── embeddings/        # Vector embeddings
└── static/                # Static files
```

## 🤖 Features

- **Multi-Model Support**: OpenAI GPT-3.5/GPT-4 and Llama 3 (7B/8B)
- **Advanced PDF Processing**: Text, images, and table extraction
- **Vector Search**: ChromaDB for semantic similarity search
- **Dynamic API Keys**: Input API keys directly in the UI
- **Portfolio Integration**: Clean, modern UI design
- **Docker Support**: Easy deployment with Docker

## 📖 Documentation

- [Complete Documentation](docs/README.md)
- [Multi-Model Guide](docs/MULTI_MODEL_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [UI Updates](docs/UI_UPDATES.md)

## 🛠️ Development

```bash
# Run tests
python tests/verify_setup.py

# Test models
python scripts/test_models.py

# Setup Ollama (for Llama 3)
./scripts/setup_ollama.sh
```

## 📄 License

This project is part of the portfolio at [www.sameetsonawane.com](https://www.sameetsonawane.com)
