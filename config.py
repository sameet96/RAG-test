import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# File Storage Configuration
UPLOAD_FOLDER = "uploads"
EMBEDDINGS_FOLDER = "embeddings"

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Vector Database Configuration
COLLECTION_NAME = "pdf_documents"
