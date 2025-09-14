import streamlit as st
import os
import uuid
from datetime import datetime
import shutil

class PDFUploader:
    def __init__(self, upload_folder="uploads"):
        self.upload_folder = upload_folder
        self.ensure_upload_folder()
    
    def ensure_upload_folder(self):
        """Create upload folder if it doesn't exist"""
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def upload_pdf(self, uploaded_file):
        """
        Upload PDF file and return file information
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: File information including path, name, size, etc.
        """
        if uploaded_file is None:
            return None
            
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{file_id}.{file_extension}"
        
        # Save file
        file_path = os.path.join(self.upload_folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Return file information
        file_info = {
            "id": file_id,
            "original_name": uploaded_file.name,
            "filename": filename,
            "file_path": file_path,
            "size": uploaded_file.size,
            "upload_time": datetime.now().isoformat(),
            "type": uploaded_file.type
        }
        
        return file_info
    
    def get_uploaded_files(self):
        """Get list of all uploaded files"""
        if not os.path.exists(self.upload_folder):
            return []
        
        files = []
        for filename in os.listdir(self.upload_folder):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.upload_folder, filename)
                file_info = {
                    "filename": filename,
                    "file_path": file_path,
                    "size": os.path.getsize(file_path),
                    "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                files.append(file_info)
        
        return files
    
    def delete_file(self, filename):
        """Delete uploaded file"""
        file_path = os.path.join(self.upload_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def cleanup_old_files(self, days=7):
        """Clean up files older than specified days"""
        if not os.path.exists(self.upload_folder):
            return
        
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.getmtime(file_path) < cutoff_time:
                os.remove(file_path)
