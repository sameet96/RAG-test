import chromadb
from chromadb.config import Settings
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
from typing import List, Dict, Any
import logging
from config import EMBEDDING_MODEL, COLLECTION_NAME, EMBEDDINGS_FOLDER

logger = logging.getLogger(__name__)

class EmbeddingSystem:
    def __init__(self, persist_directory=EMBEDDINGS_FOLDER):
        self.persist_directory = persist_directory
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Embedding system initialized with model: {EMBEDDING_MODEL}")
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            numpy array of embeddings
        """
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def store_document_chunks(self, file_id: str, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store document chunks with embeddings in ChromaDB
        
        Args:
            file_id: Unique identifier for the document
            chunks: List of content chunks
            
        Returns:
            bool: Success status
        """
        try:
            # Extract texts for embedding
            texts = [chunk["content"] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Prepare data for ChromaDB
            ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                metadata = {
                    "file_id": file_id,
                    "chunk_index": i,
                    "type": chunk["type"],
                    "page": chunk.get("page", 0),
                    "source": chunk.get("source", "unknown")
                }
                
                # Add type-specific metadata
                if chunk["type"] == "table":
                    metadata["columns"] = json.dumps(chunk.get("columns", []))
                    metadata["table_data"] = json.dumps(chunk.get("table_data", []))
                elif chunk["type"] == "image_ocr":
                    metadata["image_info"] = json.dumps(chunk.get("image_info", {}))
                
                metadatas.append(metadata)
            
            # Store in ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Stored {len(chunks)} chunks for file {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing document chunks: {str(e)}")
            return False
    
    def search_similar_chunks(self, query: str, file_id: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks based on query
        
        Args:
            query: Search query
            file_id: Optional file ID to limit search
            top_k: Number of top results to return
            
        Returns:
            List of similar chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            # Prepare where clause for filtering
            where_clause = {}
            if file_id:
                where_clause["file_id"] = file_id
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                where=where_clause if where_clause else None
            )
            
            # Format results
            similar_chunks = []
            if results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    chunk_data = {
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if results["distances"] else 0,
                        "id": results["ids"][0][i]
                    }
                    
                    # Parse JSON metadata
                    if "columns" in chunk_data["metadata"]:
                        chunk_data["metadata"]["columns"] = json.loads(chunk_data["metadata"]["columns"])
                    if "table_data" in chunk_data["metadata"]:
                        chunk_data["metadata"]["table_data"] = json.loads(chunk_data["metadata"]["table_data"])
                    if "image_info" in chunk_data["metadata"]:
                        chunk_data["metadata"]["image_info"] = json.loads(chunk_data["metadata"]["image_info"])
                    
                    similar_chunks.append(chunk_data)
            
            logger.info(f"Found {len(similar_chunks)} similar chunks for query")
            return similar_chunks
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {str(e)}")
            return []
    
    def get_document_chunks(self, file_id: str) -> List[Dict[str, Any]]:
        """
        Get all chunks for a specific document
        
        Args:
            file_id: Document file ID
            
        Returns:
            List of document chunks
        """
        try:
            results = self.collection.get(
                where={"file_id": file_id}
            )
            
            chunks = []
            if results["documents"]:
                for i in range(len(results["documents"])):
                    chunk_data = {
                        "content": results["documents"][i],
                        "metadata": results["metadatas"][i],
                        "id": results["ids"][i]
                    }
                    
                    # Parse JSON metadata
                    if "columns" in chunk_data["metadata"]:
                        chunk_data["metadata"]["columns"] = json.loads(chunk_data["metadata"]["columns"])
                    if "table_data" in chunk_data["metadata"]:
                        chunk_data["metadata"]["table_data"] = json.loads(chunk_data["metadata"]["table_data"])
                    if "image_info" in chunk_data["metadata"]:
                        chunk_data["metadata"]["image_info"] = json.loads(chunk_data["metadata"]["image_info"])
                    
                    chunks.append(chunk_data)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error getting document chunks: {str(e)}")
            return []
    
    def delete_document(self, file_id: str) -> bool:
        """
        Delete all chunks for a specific document
        
        Args:
            file_id: Document file ID
            
        Returns:
            bool: Success status
        """
        try:
            # Get all chunk IDs for the document
            results = self.collection.get(
                where={"file_id": file_id}
            )
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} chunks for file {file_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            
            # Get unique file IDs
            results = self.collection.get()
            file_ids = set()
            if results["metadatas"]:
                for metadata in results["metadatas"]:
                    if "file_id" in metadata:
                        file_ids.add(metadata["file_id"])
            
            return {
                "total_chunks": count,
                "unique_documents": len(file_ids),
                "file_ids": list(file_ids)
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"total_chunks": 0, "unique_documents": 0, "file_ids": []}
    
    def clear_collection(self) -> bool:
        """
        Clear all data from the collection
        
        Returns:
            bool: Success status
        """
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info("Collection cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            return False
