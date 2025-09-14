# 🤖 AI PDF Chat | Portfolio Project

A modern, professional RAG-based PDF Chat application with a stunning portfolio-style UI. Upload PDF documents and ask questions about their content using AI-powered retrieval and generation with a beautiful, responsive interface.

## ✨ Features

### 🎨 **Modern Portfolio UI**
- **Glass Morphism Design**: Translucent cards with backdrop blur effects
- **Gradient Headers**: Eye-catching purple-blue gradient themes
- **Professional Typography**: Clean Inter font throughout
- **Responsive Layout**: Works perfectly on all devices
- **Interactive Animations**: Smooth hover effects and transitions
- **Portfolio Branding**: Integrated with your personal portfolio

### 🔧 **Core Functionality**
- 📄 **Smart PDF Processing**: Extract text, images, and tables with advanced OCR
- 🧠 **RAG Technology**: Retrieval-Augmented Generation for intelligent responses
- 💬 **Natural Conversations**: Ask questions in natural language
- 📊 **Multi-Document Support**: Handle multiple PDFs simultaneously
- 🔍 **Semantic Search**: Vector-based similarity search using embeddings
- 🤖 **Multiple AI Models**: Support for OpenAI GPT and Llama 3 models
- 🔑 **Dynamic API Keys**: Secure API key input directly in the UI

## 🛠️ Technology Stack

### **Frontend & UI**
- **Streamlit**: Modern web framework with custom CSS
- **Google Fonts**: Inter font family for professional typography
- **CSS3**: Glass morphism, gradients, and animations

### **Backend & AI**
- **PDF Processing**: PyMuPDF, pdfplumber, PyPDF2
- **OCR**: Tesseract, OpenCV for image text extraction
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB for similarity search
- **AI Models**: 
  - OpenAI GPT-3.5-turbo & GPT-4
  - Llama 3 7B & 8B (via Ollama)
- **Local LLM**: Ollama for running models locally
- **Data Processing**: Pandas, NumPy for data manipulation

### **Deployment**
- **Docker**: Containerized deployment with Docker Compose
- **Nginx**: Reverse proxy for production deployment
- **SSL**: HTTPS support with Let's Encrypt

## 🚀 Quick Start

### **Option 1: Local Development**
```bash
# Clone the repository
git clone <repository-url>
cd RAG-test

# Set up virtual environment
python -m venv rag-project-env
source rag-project-env/bin/activate  # On Windows: rag-project-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your OpenAI API key

# Run the application
python run.py
```

### **Option 2: Docker Deployment**
```bash
# Quick deployment
./deploy.sh development

# Production deployment with nginx
./deploy.sh production
```

### **Option 3: Preview UI Only**
```bash
# Preview the new portfolio-style design
streamlit run preview_ui.py
```

## 📋 Prerequisites

### **Required Software**
- **Python 3.11+**
- **Tesseract OCR**

**Install Tesseract**:
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### **API Keys & Models**
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- **Ollama Installation**: Run `./setup_ollama.sh` for local Llama 3 models

## 💻 Usage

### **Getting Started**
1. **Launch the Application**:
   ```bash
   python run.py
   # or
   streamlit run app.py
   ```

2. **Configure AI Model**:
   - **For OpenAI**: Select OpenAI model and enter your API key in the sidebar
   - **For Llama 3**: Run `./setup_ollama.sh` first, then select Llama 3 model
   - Test your model connection using the "Test Model" button

3. **Upload & Process PDFs**:
   - Use the sidebar file uploader to upload PDF documents
   - Click "Process Document" to parse and index content
   - Wait for processing to complete (progress shown in real-time)

4. **Chat with Your Documents**:
   - Type questions in the chat interface
   - Get intelligent AI responses based on document content
   - View sources to see where information originated
   - Switch between multiple documents if uploaded

### **AI Model Selection**
Choose from multiple AI models based on your needs:

#### **OpenAI Models** (Cloud-based)
- **GPT-3.5-turbo**: Fast, cost-effective, good for most tasks
- **GPT-4**: Most capable, best for complex reasoning
- **Setup**: Enter your OpenAI API key in the sidebar

#### **Llama 3 Models** (Local)
- **Llama 3 7B**: Fast local inference, good balance of speed/quality
- **Llama 3 8B**: Better quality, slightly slower
- **Setup**: Run `./setup_ollama.sh` to install Ollama and models

### **Sample Questions**
- "What is the main topic of this document?"
- "Can you summarize the key points?"
- "What are the important dates mentioned?"
- "Are there any tables or data I should know about?"
- "What conclusions does the author draw?"

## 🎨 Portfolio Integration

### **Embed in Your Portfolio**
This application is designed to seamlessly integrate with your portfolio website:

- **Standalone Page**: Use `portfolio-integration.html` as a dedicated page
- **Embedded Widget**: Use `portfolio-integration.js` for inline integration
- **React Component**: Use the provided React component for React-based portfolios

### **Customization**
- **Colors**: Update gradient colors in CSS files
- **Branding**: Add your logo and personal links
- **Domain**: Configure custom domain for deployment

## 📁 Project Structure

```
RAG-test/
├── 🎨 UI & Styling
│   ├── app.py                    # Main Streamlit application with portfolio UI
│   ├── preview_ui.py            # UI preview script
│   ├── .streamlit/
│   │   ├── config.toml          # Streamlit theme configuration
│   │   └── style.css            # Additional custom styling
│   └── portfolio-integration.*  # Portfolio integration files
├── 🔧 Core Application
│   ├── config.py                # Configuration settings
│   ├── pdf_uploader.py          # PDF upload and file management
│   ├── pdf_parser.py            # PDF parsing (text, images, tables)
│   ├── embedding_system.py      # Embedding generation and vector storage
│   ├── rag_system.py            # RAG pipeline and OpenAI integration
│   └── run.py                   # Application startup script
├── 🐳 Deployment
│   ├── Dockerfile               # Docker container configuration
│   ├── docker-compose.yml       # Multi-service orchestration
│   ├── nginx.conf               # Reverse proxy configuration
│   ├── deploy.sh                # Automated deployment script
│   └── .dockerignore            # Docker build context optimization
├── 📚 Documentation
│   ├── README.md                # This comprehensive guide
│   ├── DEPLOYMENT.md            # Detailed deployment instructions
│   ├── PORTFOLIO_INTEGRATION_GUIDE.md  # Integration guide
│   ├── UI_UPDATES.md            # UI design documentation
│   └── .gitignore               # Git ignore rules
├── ⚙️ Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── env.example              # Environment variables template
│   ├── setup_env.sh             # Environment setup script
│   └── test-local.sh            # Local testing script
└── 📂 Data Directories (auto-created)
    ├── uploads/                 # Uploaded PDF files
    ├── embeddings/              # Vector database storage
    └── chroma_db/               # ChromaDB persistence
```

## 🔄 How It Works

### **RAG Pipeline**
1. **📄 Document Upload**: PDF files are uploaded and stored securely
2. **🔍 Content Parsing**: 
   - Text extraction from each page
   - Image processing with OCR (Tesseract)
   - Table extraction and conversion to text
3. **✂️ Intelligent Chunking**: Content split into manageable chunks with overlap
4. **🧠 Embedding Generation**: Each chunk converted to vector embeddings
5. **💾 Vector Storage**: Embeddings stored in ChromaDB for fast retrieval
6. **❓ Query Processing**: User questions converted to embeddings
7. **🔍 Similarity Search**: Relevant chunks retrieved based on similarity
8. **🤖 Answer Generation**: OpenAI GPT generates answers using retrieved context

### **UI Architecture**
- **Frontend**: Streamlit with custom CSS and JavaScript
- **Styling**: Glass morphism, gradients, and animations
- **Responsive**: Mobile-first design with adaptive layouts
- **Interactive**: Real-time updates and smooth transitions

## 🌐 Deployment Options

### **Local Development**
```bash
python run.py
# Access at: http://localhost:8501
```

### **Docker Development**
```bash
./deploy.sh development
# Access at: http://localhost:8501
```

### **Production Deployment**
```bash
./deploy.sh production
# Access at: http://localhost (with nginx)
```

### **Cloud Deployment**
- **AWS**: EC2 with Docker
- **Google Cloud**: Cloud Run or Compute Engine
- **Azure**: Container Instances
- **Heroku**: Container deployment
- **DigitalOcean**: Droplet with Docker

## 🔧 Configuration

### **Environment Variables**
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### **Customization Options**
- **Embedding Model**: Change in `config.py`
- **Chunk Size**: Adjust for better precision/recall
- **UI Colors**: Modify CSS gradient colors
- **Branding**: Update footer links and text

## 🚨 Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| **Tesseract not found** | Install Tesseract and add to PATH |
| **OpenAI API errors** | Check API key and credits |
| **Memory issues** | Reduce chunk size in config.py |
| **Slow processing** | Use GPU for embedding generation |
| **Docker build fails** | Check Docker installation and permissions |
| **Port conflicts** | Change port in docker-compose.yml |

### **Performance Optimization**
- **Chunk Size**: Smaller = better precision, larger = better context
- **Chunk Overlap**: Increase for better continuity
- **Batch Processing**: Process large files in batches
- **GPU Usage**: Enable GPU for faster embeddings
- **Caching**: Clear old embeddings periodically

## 📊 Monitoring & Analytics

### **Application Metrics**
- Document processing time
- Query response time
- Memory usage
- API call costs
- User engagement

### **Health Checks**
```bash
# Check application status
curl -f http://localhost:8501/_stcore/health

# Docker container status
docker-compose ps

# View logs
docker-compose logs -f rag-app
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Add tests** if applicable
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Submit a pull request**

### **Development Guidelines**
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test changes locally before submitting
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the GPT models and API
- **ChromaDB** for vector storage capabilities
- **Streamlit** for the amazing web framework
- **Sentence Transformers** for embedding models
- **PyMuPDF** for PDF processing
- **The open-source community** for all the wonderful libraries

## 📞 Support & Contact

- **Portfolio**: [www.sameetsonawane.com](https://www.sameetsonawane.com)
- **GitHub**: [github.com/sameetsonawane](https://github.com/sameetsonawane)
- **Issues**: Create an issue in this repository

---

**Built with ❤️ by Sameet Sonawane** | **Powered by OpenAI GPT, ChromaDB, and Streamlit**
