import streamlit as st
import os
import time
from typing import Dict, Any
import logging

# Import our custom modules
from pdf_uploader import PDFUploader
from rag_system import RAGSystem
from config import UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI PDF Chat | Sameet Sonawane",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "rag_system" not in st.session_state:
    st.session_state.rag_system = RAGSystem()

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def inject_custom_css():
    """Inject custom CSS for portfolio-style design"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main container styling */
    .main {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .portfolio-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .portfolio-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .portfolio-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
        margin-bottom: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed #667eea;
        border-radius: 10px;
        background: rgba(102, 126, 234, 0.05);
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #764ba2;
        background: rgba(118, 75, 162, 0.1);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Chat input styling */
    .stChatInput > div > div > div {
        border-radius: 25px;
        border: 2px solid #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 0 10px 10px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 15px;
        border: none;
        backdrop-filter: blur(10px);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-card h3 {
        color: #667eea;
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        margin: 0;
    }
    
    .metric-card p {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-card h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.8);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Portfolio-style header
    st.markdown("""
    <div class="portfolio-header">
        <h1>🤖 AI PDF Chat</h1>
        <p>Intelligent Document Analysis & Q&A System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h3>Smart PDF Processing</h3>
            <p>Extract text, images, and tables from PDF documents with advanced OCR capabilities</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3>RAG Technology</h3>
            <p>Retrieval-Augmented Generation system that understands document context</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Natural Conversations</h3>
            <p>Ask questions in natural language and get intelligent responses</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for file management
    with st.sidebar:
        st.markdown("### 🤖 Model Configuration")
        
        # Model selection
        rag_system = st.session_state.rag_system
        available_models = rag_system.get_available_models()
        
        # Filter models based on availability
        model_options = []
        for model_name, model_info in available_models.items():
            if model_info["provider"] == "ollama":
                # Check if Ollama is available
                model_status = rag_system.get_model_status()
                if model_status.get("ollama_available", False):
                    model_options.append(model_name)
            else:
                model_options.append(model_name)
        
        if model_options:
            selected_model = st.selectbox(
                "Select AI Model",
                options=model_options,
                help="Choose the AI model for generating responses"
            )
            
            # API Key input for OpenAI models
            api_key = None
            if selected_model.startswith("OpenAI"):
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    help="Enter your OpenAI API key",
                    placeholder="sk-..."
                )
            
            # Model status and test
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Set Model", type="primary"):
                    with st.spinner("Setting up model..."):
                        success = rag_system.set_model(selected_model, api_key)
                        if success:
                            st.success("Model set successfully!")
                        else:
                            st.error("Failed to set model. Check your configuration.")
            
            with col2:
                if st.button("Test Model"):
                    with st.spinner("Testing model..."):
                        test_result = rag_system.test_model_connection()
                        if test_result["success"]:
                            st.success("✅ Model working!")
                        else:
                            st.error(f"❌ {test_result['message']}")
            
            # Show current model status
            model_status = rag_system.get_model_status()
            if model_status["current_model"]:
                st.info(f"**Current Model:** {model_status['current_model']}")
        else:
            st.warning("No models available. Please check your configuration.")
        
        st.markdown("---")
        st.markdown("### 📁 Document Management")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload a PDF file",
            type=['pdf'],
            help="Upload a PDF document to start asking questions",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    # Upload file
                    uploader = PDFUploader(UPLOAD_FOLDER)
                    file_info = uploader.upload_pdf(uploaded_file)
                    
                    if file_info:
                        # Process document with RAG system
                        success = st.session_state.rag_system.process_document(
                            file_info["id"], 
                            file_info["file_path"]
                        )
                        
                        if success:
                            st.success(f"✅ Document '{uploaded_file.name}' processed successfully!")
                            st.session_state.uploaded_files[file_info["id"]] = file_info
                            
                            # Clear chat history when new document is processed
                            st.session_state.chat_history = []
                        else:
                            st.error("❌ Failed to process document. Please try again.")
                    else:
                        st.error("❌ Failed to upload file.")
        
        # Display uploaded files
        if st.session_state.uploaded_files:
            st.subheader("📋 Processed Documents")
            for file_id, file_info in st.session_state.uploaded_files.items():
                with st.expander(f"📄 {file_info['original_name']}"):
                    st.write(f"**Size:** {file_info['size']:,} bytes")
                    st.write(f"**Uploaded:** {file_info['upload_time']}")
                    
                    # Show document summary
                    summary = st.session_state.rag_system.get_document_summary(file_id)
                    if "error" not in summary:
                        st.write(f"**Pages:** {summary['total_pages']}")
                        st.write(f"**Chunks:** {summary['total_chunks']}")
                        st.write(f"**Content Types:** {summary['content_types']}")
                    
                    if st.button(f"🗑️ Delete", key=f"delete_{file_id}"):
                        if st.session_state.rag_system.delete_document(file_id):
                            del st.session_state.uploaded_files[file_id]
                            st.success("Document deleted successfully!")
                            st.rerun()
        
        # System stats
        st.markdown("### 📊 System Statistics")
        stats = st.session_state.rag_system.get_system_stats()
        if "error" not in stats:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{stats['unique_documents']}</h3>
                    <p>Documents</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{stats['total_chunks']}</h3>
                    <p>Chunks</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Model status
            model_status = rag_system.get_model_status()
            model_icon = "✅" if model_status['current_model'] else "❌"
            model_name = model_status['current_model'] or "Not Set"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{model_icon}</h3>
                <p>Model: {model_name[:20]}{'...' if len(model_name) > 20 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Error loading stats: {stats['error']}")
    
    # Main chat interface
    st.markdown("## 💬 Chat with Your Documents")
    
    # Check if any documents are processed
    if not st.session_state.uploaded_files:
        st.info("👆 Please upload and process a PDF document first to start chatting!")
        
        # Show sample questions
        st.markdown("### 💡 Sample Questions You Can Ask:")
        sample_questions = [
            "What is the main topic of this document?",
            "Can you summarize the key points?",
            "What are the important dates mentioned?",
            "Are there any tables or data I should know about?",
            "What conclusions does the author draw?"
        ]
        
        for question in sample_questions:
            st.markdown(f"• {question}")
        
        return
    
    # Document selection
    if len(st.session_state.uploaded_files) > 1:
        file_options = {f"{info['original_name']}": file_id 
                       for file_id, info in st.session_state.uploaded_files.items()}
        selected_file = st.selectbox(
            "Select document to query:",
            options=list(file_options.keys()),
            help="Choose which document to ask questions about"
        )
        selected_file_id = file_options[selected_file]
    else:
        selected_file_id = list(st.session_state.uploaded_files.keys())[0]
        selected_file_name = list(st.session_state.uploaded_files.values())[0]['original_name']
        st.info(f"📄 Chatting with: **{selected_file_name}**")
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Show sources if available
                    if "sources" in message and message["sources"]:
                        with st.expander("📚 Sources"):
                            for j, source in enumerate(message["sources"]):
                                st.write(f"**Source {j+1}:** Page {source['page']}, Type: {source['type']}")
    
    # Chat input
    user_input = st.chat_input("Ask a question about your document...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.rag_system.search_and_answer(
                user_input, 
                selected_file_id, 
                top_k=5
            )
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response["answer"],
            "sources": response["sources"]
        })
        
        # Display assistant response
        with chat_container:
            with st.chat_message("assistant"):
                st.write(response["answer"])
                
                # Show sources
                if response["sources"]:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(response["sources"]):
                            st.write(f"**Source {i+1}:** Page {source['page']}, Type: {source['type']}")
                            
                            # Show additional info for tables
                            if source["type"] == "table" and "columns" in source:
                                st.write(f"Columns: {', '.join(source['columns'])}")
        
        # Rerun to update the display
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

def show_help():
    """Show help information"""
    st.markdown("""
    <div class="feature-card">
        <h2>🚀 How to use this application</h2>
        <ol>
            <li><strong>Upload a PDF</strong>: Use the sidebar to upload a PDF document</li>
            <li><strong>Process Document</strong>: Click "Process Document" to parse and index the content</li>
            <li><strong>Ask Questions</strong>: Type your questions in the chat interface</li>
            <li><strong>View Sources</strong>: Click on "Sources" to see where the information came from</li>
        </ol>
        
        <h3>✨ Features</h3>
        <ul>
            <li>📄 <strong>Text Extraction</strong>: Extracts text from PDF pages</li>
            <li>🖼️ <strong>Image OCR</strong>: Extracts text from images using OCR</li>
            <li>📊 <strong>Table Parsing</strong>: Extracts and processes tables</li>
            <li>🔍 <strong>Semantic Search</strong>: Finds relevant content using embeddings</li>
            <li>🤖 <strong>AI Answers</strong>: Generates answers using OpenAI GPT</li>
        </ul>
        
        <h3>💡 Tips</h3>
        <ul>
            <li>Ask specific questions for better results</li>
            <li>Reference page numbers or specific content</li>
            <li>The system can handle multiple documents</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def add_portfolio_footer():
    """Add portfolio-style footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7);">
        <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem; margin: 0;">
            Built with ❤️ by <strong>Sameet Sonawane</strong> | 
            <a href="https://www.sameetsonawane.com" style="color: #667eea; text-decoration: none;">Portfolio</a> | 
            <a href="https://github.com/sameetsonawane" style="color: #667eea; text-decoration: none;">GitHub</a>
        </p>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.8rem; margin: 0.5rem 0 0 0; opacity: 0.6;">
            Powered by OpenAI GPT, ChromaDB, and Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Add help button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("❓ Help", use_container_width=True):
            show_help()
    
    main()
    
    # Add portfolio footer
    add_portfolio_footer()
