# RAG-based PDF Chat Application

A comprehensive Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content using AI-powered search and text generation.

## Features

- 📄 **PDF Upload & Storage**: Secure file upload and management
- 🔍 **Advanced PDF Parsing**: 
  - Text extraction from pages
  - Image OCR using Tesseract
  - Table extraction and processing
- 🧠 **Semantic Search**: Vector-based similarity search using embeddings
- 🤖 **AI-Powered Answers**: Integration with OpenAI GPT for intelligent responses
- 💬 **Interactive Chat Interface**: Clean, user-friendly chat interface
- 📊 **Multi-Document Support**: Handle multiple PDFs simultaneously

## Technology Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyMuPDF, pdfplumber
- **OCR**: Tesseract, OpenCV
- **Embeddings**: Sentence Transformers
- **Vector Database**: ChromaDB
- **AI**: OpenAI GPT-3.5-turbo
- **Data Processing**: Pandas, NumPy

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd RAG-test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   
   **On macOS**:
   ```bash
   brew install tesseract
   ```
   
   **On Ubuntu/Debian**:
   ```bash
   sudo apt-get install tesseract-ocr
   ```
   
   **On Windows**:
   Download from: https://github.com/UB-Mannheim/tesseract/wiki

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF**:
   - Use the sidebar to upload a PDF document
   - Click "Process Document" to parse and index the content

3. **Ask Questions**:
   - Type your questions in the chat interface
   - The system will search for relevant content and generate answers
   - View sources to see where information came from

## Configuration

Edit `config.py` to customize:

- **Embedding Model**: Change the sentence transformer model
- **Chunk Size**: Adjust text chunk size for processing
- **Chunk Overlap**: Set overlap between chunks
- **Storage Paths**: Modify upload and embedding directories

## Project Structure

```
RAG-test/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── pdf_uploader.py       # PDF upload and file management
├── pdf_parser.py         # PDF parsing (text, images, tables)
├── embedding_system.py   # Embedding generation and vector storage
├── rag_system.py         # RAG pipeline and OpenAI integration
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── uploads/             # Uploaded PDF files (created automatically)
└── embeddings/          # Vector database storage (created automatically)
```

## How It Works

1. **Document Upload**: PDF files are uploaded and stored securely
2. **Content Parsing**: 
   - Text is extracted from each page
   - Images are processed with OCR
   - Tables are extracted and converted to text
3. **Chunking**: Content is split into manageable chunks with overlap
4. **Embedding Generation**: Each chunk is converted to vector embeddings
5. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
6. **Query Processing**: User questions are converted to embeddings
7. **Similarity Search**: Relevant chunks are retrieved based on similarity
8. **Answer Generation**: OpenAI GPT generates answers using retrieved context

## API Integration

The application uses OpenAI's GPT-3.5-turbo for text generation. Make sure to:
- Get an API key from OpenAI
- Add it to your `.env` file
- Ensure you have sufficient API credits

## Troubleshooting

### Common Issues:

1. **Tesseract not found**: Make sure Tesseract is installed and in your PATH
2. **OpenAI API errors**: Check your API key and credits
3. **Memory issues**: Reduce chunk size in config.py for large documents
4. **Slow processing**: Consider using a GPU for embedding generation

### Performance Tips:

- Use smaller chunk sizes for better precision
- Increase chunk overlap for better context
- Process documents in batches for large files
- Clear old embeddings periodically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the GPT models
- ChromaDB for vector storage
- Streamlit for the web interface
- The open-source community for the various libraries used
