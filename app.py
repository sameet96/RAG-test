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
    page_title="RAG PDF Chat",
    page_icon="📚",
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

def main():
    st.title("📚 RAG-based PDF Chat Application")
    st.markdown("Upload PDF documents and ask questions about their content using AI-powered retrieval and generation.")
    
    # Sidebar for file management
    with st.sidebar:
        st.header("📁 Document Management")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload a PDF file",
            type=['pdf'],
            help="Upload a PDF document to start asking questions"
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
        st.subheader("📊 System Statistics")
        stats = st.session_state.rag_system.get_system_stats()
        if "error" not in stats:
            st.write(f"**Total Documents:** {stats['unique_documents']}")
            st.write(f"**Total Chunks:** {stats['total_chunks']}")
            st.write(f"**OpenAI Configured:** {'✅' if stats['openai_configured'] else '❌'}")
        else:
            st.error(f"Error loading stats: {stats['error']}")
    
    # Main chat interface
    st.header("💬 Chat with Your Documents")
    
    # Check if any documents are processed
    if not st.session_state.uploaded_files:
        st.info("👆 Please upload and process a PDF document first to start chatting!")
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
    ## How to use this application:
    
    1. **Upload a PDF**: Use the sidebar to upload a PDF document
    2. **Process Document**: Click "Process Document" to parse and index the content
    3. **Ask Questions**: Type your questions in the chat interface
    4. **View Sources**: Click on "Sources" to see where the information came from
    
    ## Features:
    - 📄 **Text Extraction**: Extracts text from PDF pages
    - 🖼️ **Image OCR**: Extracts text from images using OCR
    - 📊 **Table Parsing**: Extracts and processes tables
    - 🔍 **Semantic Search**: Finds relevant content using embeddings
    - 🤖 **AI Answers**: Generates answers using OpenAI GPT
    
    ## Tips:
    - Ask specific questions for better results
    - Reference page numbers or specific content
    - The system can handle multiple documents
    """)

if __name__ == "__main__":
    # Add help button
    if st.button("❓ Help"):
        show_help()
    
    main()
