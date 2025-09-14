"""
Core functionality for the RAG PDF Chat Application.

This package contains the main components:
- RAGSystem: Main RAG orchestration
- ModelManager: Multi-model management (OpenAI, Ollama)
- EmbeddingSystem: Vector embeddings and similarity search
- PDFParser: PDF processing and content extraction
"""

from .rag_system import RAGSystem
from .model_manager import ModelManager
from .embedding_system import EmbeddingSystem
from .pdf_parser import PDFParser

__all__ = ['RAGSystem', 'ModelManager', 'EmbeddingSystem', 'PDFParser']
