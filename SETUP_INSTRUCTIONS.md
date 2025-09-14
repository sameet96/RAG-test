# RAG PDF Chat Application - Setup Instructions

## ✅ Environment Setup Complete!

Your RAG project environment has been successfully created and configured. Here's what was set up:

### 📁 Project Structure
```
RAG-test/
├── app.py                    # Main Streamlit application
├── config.py                # Configuration settings
├── pdf_uploader.py          # PDF upload functionality
├── pdf_parser.py            # PDF parsing (text, images, tables)
├── embedding_system.py      # Embedding generation and storage
├── rag_system.py            # RAG pipeline and OpenAI integration
├── run.py                   # Startup script with dependency checks
├── setup_env.sh            # Environment setup script
├── requirements_minimal.txt # Working dependencies
├── environment.yml          # Conda environment specification
├── .env                     # Environment variables (API keys)
├── uploads/                 # PDF storage directory (auto-created)
├── embeddings/              # Vector database storage (auto-created)
└── rag-project-env/         # Python virtual environment
```

### 🚀 How to Run the Application

1. **Activate the environment**:
   ```bash
   source rag-project-env/bin/activate
   ```

2. **Set up your OpenAI API key**:
   Edit the `.env` file and replace `your_openai_api_key_here` with your actual API key:
   ```bash
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

4. **Access the application**:
   Open your browser and go to: `http://localhost:8501`

### 📋 Features Available

- ✅ **PDF Upload**: Upload PDF documents through the web interface
- ✅ **Text Extraction**: Extract text from PDF pages
- ✅ **Table Parsing**: Extract and process tables
- ✅ **OCR Support**: Extract text from images (requires Tesseract)
- ✅ **Semantic Search**: Vector-based similarity search
- ✅ **AI Chat**: Ask questions about your documents
- ✅ **Source Attribution**: See exactly where information came from
- ✅ **Multi-Document Support**: Handle multiple PDFs simultaneously

### 🔧 Troubleshooting

#### If you get "Tesseract not found" errors:
Install Tesseract OCR:
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### If you get OpenAI API errors:
1. Make sure your API key is correct in the `.env` file
2. Ensure you have sufficient API credits
3. Check your internet connection

#### If the application doesn't start:
1. Make sure you're in the correct directory
2. Activate the virtual environment: `source rag-project-env/bin/activate`
3. Check that all dependencies are installed: `pip list`

### 🎯 Usage Guide

1. **Upload a PDF**: Use the sidebar to upload a PDF document
2. **Process Document**: Click "Process Document" to parse and index the content
3. **Ask Questions**: Type your questions in the chat interface
4. **View Sources**: Click on "Sources" to see where information came from

### 📊 System Requirements

- Python 3.9+
- 4GB+ RAM recommended
- Internet connection for OpenAI API
- Tesseract OCR for image text extraction (optional)

### 🔄 Updating Dependencies

If you need to update dependencies:
```bash
source rag-project-env/bin/activate
pip install --upgrade -r requirements_minimal.txt
```

### 🆘 Need Help?

- Check the README.md for detailed documentation
- Review the console output for error messages
- Ensure all environment variables are set correctly
- Make sure your OpenAI API key is valid and has credits

---

**🎉 Your RAG PDF Chat Application is ready to use!**
