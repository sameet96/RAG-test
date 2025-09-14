import openai
from typing import List, Dict, Any
import logging
from config import OPENAI_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP
from embedding_system import EmbeddingSystem

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.embedding_system = EmbeddingSystem()
        
        # Initialize OpenAI
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        else:
            logger.warning("OpenAI API key not found. Text generation will not work.")
            self.openai_client = None
    
    def process_document(self, file_id: str, file_path: str) -> bool:
        """
        Process a document: parse, chunk, and store embeddings
        
        Args:
            file_id: Unique identifier for the document
            file_path: Path to the PDF file
            
        Returns:
            bool: Success status
        """
        try:
            from pdf_parser import PDFParser
            
            # Parse the PDF
            parser = PDFParser()
            parsed_content = parser.parse_pdf(file_path)
            
            # Chunk the content
            chunks = parser.chunk_content(
                parsed_content, 
                chunk_size=CHUNK_SIZE, 
                overlap=CHUNK_OVERLAP
            )
            
            # Store chunks with embeddings
            success = self.embedding_system.store_document_chunks(file_id, chunks)
            
            if success:
                logger.info(f"Successfully processed document {file_id} with {len(chunks)} chunks")
            else:
                logger.error(f"Failed to store embeddings for document {file_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing document {file_id}: {str(e)}")
            return False
    
    def search_and_answer(self, query: str, file_id: str = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Search for relevant content and generate an answer
        
        Args:
            query: User's question
            file_id: Optional file ID to limit search
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            Dictionary with answer and context
        """
        try:
            # Search for similar chunks
            similar_chunks = self.embedding_system.search_similar_chunks(
                query, file_id, top_k
            )
            
            if not similar_chunks:
                return {
                    "answer": "I couldn't find any relevant information in the uploaded documents to answer your question.",
                    "context": [],
                    "sources": []
                }
            
            # Prepare context for the LLM
            context_parts = []
            sources = []
            
            for chunk in similar_chunks:
                content = chunk["content"]
                metadata = chunk["metadata"]
                
                # Add source information
                source_info = {
                    "page": metadata.get("page", "Unknown"),
                    "type": metadata.get("type", "text"),
                    "chunk_index": metadata.get("chunk_index", 0)
                }
                
                # Add type-specific information
                if metadata.get("type") == "table":
                    source_info["columns"] = metadata.get("columns", [])
                elif metadata.get("type") == "image_ocr":
                    source_info["image_info"] = metadata.get("image_info", {})
                
                sources.append(source_info)
                
                # Format context with source information
                context_text = f"[Page {metadata.get('page', 'Unknown')}, {metadata.get('type', 'text')}]: {content}"
                context_parts.append(context_text)
            
            # Combine context
            context = "\n\n".join(context_parts)
            
            # Generate answer using OpenAI
            if self.openai_client:
                answer = self._generate_answer_with_openai(query, context)
            else:
                answer = "OpenAI API key not configured. Cannot generate answer."
            
            return {
                "answer": answer,
                "context": context_parts,
                "sources": sources,
                "similar_chunks": similar_chunks
            }
            
        except Exception as e:
            logger.error(f"Error in search and answer: {str(e)}")
            return {
                "answer": f"Sorry, I encountered an error while processing your question: {str(e)}",
                "context": [],
                "sources": []
            }
    
    def _generate_answer_with_openai(self, query: str, context: str) -> str:
        """
        Generate answer using OpenAI GPT
        
        Args:
            query: User's question
            context: Retrieved context from documents
            
        Returns:
            Generated answer
        """
        try:
            prompt = f"""Based on the following context from uploaded documents, please answer the user's question. 
If the answer cannot be found in the context, please say so clearly.

Context:
{context}

Question: {query}

Answer:"""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that answers questions based on provided document context. Be accurate and cite specific information from the context when possible."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer with OpenAI: {str(e)}")
            return f"Error generating answer: {str(e)}"
    
    def get_document_summary(self, file_id: str) -> Dict[str, Any]:
        """
        Get a summary of a document
        
        Args:
            file_id: Document file ID
            
        Returns:
            Document summary information
        """
        try:
            chunks = self.embedding_system.get_document_chunks(file_id)
            
            if not chunks:
                return {"error": "Document not found or has no chunks"}
            
            # Count different content types
            type_counts = {}
            total_pages = set()
            
            for chunk in chunks:
                chunk_type = chunk["metadata"].get("type", "unknown")
                type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1
                
                page = chunk["metadata"].get("page", 0)
                if page:
                    total_pages.add(page)
            
            # Get sample content
            sample_texts = []
            for chunk in chunks[:3]:  # First 3 chunks
                content = chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
                sample_texts.append(content)
            
            return {
                "total_chunks": len(chunks),
                "total_pages": len(total_pages),
                "content_types": type_counts,
                "sample_content": sample_texts
            }
            
        except Exception as e:
            logger.error(f"Error getting document summary: {str(e)}")
            return {"error": str(e)}
    
    def delete_document(self, file_id: str) -> bool:
        """
        Delete a document and its embeddings
        
        Args:
            file_id: Document file ID
            
        Returns:
            bool: Success status
        """
        try:
            return self.embedding_system.delete_document(file_id)
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get system statistics
        
        Returns:
            Dictionary with system stats
        """
        try:
            collection_stats = self.embedding_system.get_collection_stats()
            
            return {
                "embedding_model": "all-MiniLM-L6-v2",
                "chunk_size": CHUNK_SIZE,
                "chunk_overlap": CHUNK_OVERLAP,
                "openai_configured": self.openai_client is not None,
                **collection_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {str(e)}")
            return {"error": str(e)}
