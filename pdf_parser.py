import pdfplumber
import pytesseract
import numpy as np
from PIL import Image
import pandas as pd
import io
import os
from typing import List, Dict, Any
import logging

# Try to import PyMuPDF, fall back to alternatives if not available
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    logging.warning("PyMuPDF not available. Image extraction will be limited.")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available. Some image processing features will be disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Parse PDF file and extract text, images, and tables
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            dict: Parsed content with text, images, and tables
        """
        try:
            logger.info(f"Starting to parse PDF: {file_path}")
            
            # Initialize result structure
            result = {
                "text_content": [],
                "images": [],
                "tables": [],
                "metadata": {},
                "total_pages": 0
            }
            
            # Extract using PyMuPDF for images and basic text
            result.update(self._extract_with_pymupdf(file_path))
            
            # Extract using pdfplumber for better text and tables
            result.update(self._extract_with_pdfplumber(file_path))
            
            # Process images with OCR
            result["images"] = self._process_images_with_ocr(result["images"])
            
            logger.info(f"Successfully parsed PDF with {result['total_pages']} pages")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            raise
    
    def _extract_with_pymupdf(self, file_path: str) -> Dict[str, Any]:
        """Extract content using PyMuPDF"""
        result = {
            "text_content": [],
            "images": [],
            "metadata": {},
            "total_pages": 0
        }
        
        if not PYMUPDF_AVAILABLE:
            logger.warning("PyMuPDF not available, skipping advanced extraction")
            return result
        
        try:
            doc = fitz.open(file_path)
            result["total_pages"] = len(doc)
            result["metadata"] = doc.metadata
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                if text.strip():
                    result["text_content"].append({
                        "page": page_num + 1,
                        "text": text.strip(),
                        "source": "pymupdf"
                    })
                
                # Extract images
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:  # GRAY or RGB
                            img_data = pix.tobytes("png")
                            result["images"].append({
                                "page": page_num + 1,
                                "image_index": img_index,
                                "data": img_data,
                                "format": "png",
                                "width": pix.width,
                                "height": pix.height
                            })
                        pix = None
                    except Exception as e:
                        logger.warning(f"Error extracting image {img_index} from page {page_num + 1}: {str(e)}")
                        continue
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error with PyMuPDF extraction: {str(e)}")
        
        return result
    
    def _extract_with_pdfplumber(self, file_path: str) -> Dict[str, Any]:
        """Extract content using pdfplumber for better text and tables"""
        result = {
            "text_content": [],
            "tables": []
        }
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract text with better formatting
                    text = page.extract_text()
                    if text and text.strip():
                        result["text_content"].append({
                            "page": page_num + 1,
                            "text": text.strip(),
                            "source": "pdfplumber"
                        })
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table_index, table in enumerate(tables):
                        if table and len(table) > 0:
                            # Convert table to DataFrame for better handling
                            df = pd.DataFrame(table[1:], columns=table[0])
                            
                            result["tables"].append({
                                "page": page_num + 1,
                                "table_index": table_index,
                                "data": df.to_dict('records'),
                                "columns": df.columns.tolist(),
                                "shape": df.shape,
                                "text_representation": self._table_to_text(df)
                            })
        
        except Exception as e:
            logger.error(f"Error with pdfplumber extraction: {str(e)}")
        
        return result
    
    def _process_images_with_ocr(self, images: List[Dict]) -> List[Dict]:
        """Process images with OCR to extract text"""
        processed_images = []
        
        for img_data in images:
            try:
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(img_data["data"]))
                
                # Apply OCR directly to PIL Image
                ocr_text = pytesseract.image_to_string(image)
                
                # Add OCR text to image data
                img_data["ocr_text"] = ocr_text.strip()
                img_data["has_text"] = bool(ocr_text.strip())
                
                processed_images.append(img_data)
                
            except Exception as e:
                logger.warning(f"Error processing image with OCR: {str(e)}")
                img_data["ocr_text"] = ""
                img_data["has_text"] = False
                processed_images.append(img_data)
        
        return processed_images
    
    def _table_to_text(self, df: pd.DataFrame) -> str:
        """Convert DataFrame to readable text format"""
        try:
            text_parts = []
            
            # Add column headers
            headers = " | ".join(str(col) for col in df.columns)
            text_parts.append(f"Table with columns: {headers}")
            
            # Add rows
            for index, row in df.iterrows():
                row_text = " | ".join(str(val) if pd.notna(val) else "" for val in row.values)
                text_parts.append(f"Row {index + 1}: {row_text}")
            
            return "\n".join(text_parts)
            
        except Exception as e:
            logger.warning(f"Error converting table to text: {str(e)}")
            return "Table data could not be converted to text"
    
    def chunk_content(self, parsed_content: Dict[str, Any], chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Split parsed content into chunks for embedding
        
        Args:
            parsed_content: Parsed PDF content
            chunk_size: Maximum size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            list: List of content chunks
        """
        chunks = []
        
        # Process text content
        for text_item in parsed_content["text_content"]:
            text = text_item["text"]
            page = text_item["page"]
            
            # Split text into chunks
            text_chunks = self._split_text(text, chunk_size, overlap)
            
            for i, chunk_text in enumerate(text_chunks):
                chunks.append({
                    "type": "text",
                    "content": chunk_text,
                    "page": page,
                    "chunk_index": i,
                    "source": text_item["source"]
                })
        
        # Process tables
        for table_item in parsed_content["tables"]:
            table_text = table_item["text_representation"]
            page = table_item["page"]
            
            # Split table text into chunks if needed
            table_chunks = self._split_text(table_text, chunk_size, overlap)
            
            for i, chunk_text in enumerate(table_chunks):
                chunks.append({
                    "type": "table",
                    "content": chunk_text,
                    "page": page,
                    "chunk_index": i,
                    "table_data": table_item["data"],
                    "columns": table_item["columns"]
                })
        
        # Process images with OCR text
        for img_item in parsed_content["images"]:
            if img_item.get("has_text", False):
                ocr_text = img_item["ocr_text"]
                page = img_item["page"]
                
                # Split OCR text into chunks
                ocr_chunks = self._split_text(ocr_text, chunk_size, overlap)
                
                for i, chunk_text in enumerate(ocr_chunks):
                    chunks.append({
                        "type": "image_ocr",
                        "content": chunk_text,
                        "page": page,
                        "chunk_index": i,
                        "image_info": {
                            "width": img_item["width"],
                            "height": img_item["height"]
                        }
                    })
        
        return chunks
    
    def _split_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start + chunk_size // 2, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            # If no sentence boundary found, look for word boundary
            if end < len(text):
                for i in range(end, max(start + chunk_size // 2, end - 50), -1):
                    if text[i] == ' ':
                        end = i
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
