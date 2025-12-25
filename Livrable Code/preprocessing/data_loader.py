"""Module for loading and parsing candidate documents."""
import os
import re
from typing import List, Dict, Optional
from pathlib import Path
from pypdf import PdfReader        # ✔ replaced PyPDF2
from docx import Document
import pandas as pd


class DataLoader:
    """Loads and parses candidate documents (CVs, cover letters, etc.)."""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text() or ""
                text += extracted + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def load_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return ""
    
    def load_text(self, file_path: str) -> str:
        """Load text from a .txt file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""
    
    def parse_candidate_document(self, file_path: str) -> Dict[str, str]:
        """Parse a candidate document and extract structured information."""
        file_path = Path(file_path)
        file_type = file_path.suffix.lower()
        
        if file_type == '.pdf':
            content = self.load_pdf(str(file_path))
        elif file_type == '.docx':
            content = self.load_docx(str(file_path))
        elif file_type == '.txt':
            content = self.load_text(str(file_path))
        else:
            content = ""
        
        return {
            'filename': file_path.name,
            'file_type': file_type,
            'content': content,
            'candidate_id': self._extract_candidate_id(file_path.name)
        }
    
    def _extract_candidate_id(self, filename: str) -> str:
        """Extract candidate ID from filename."""
        # Assume format: candidate_001.pdf or CV_001.pdf
        match = re.search(r'(\d+)', filename)
        return match.group(1) if match else filename.replace('.', '_')
    
    def load_all_candidates(self) -> List[Dict[str, str]]:
        """Load all candidate documents from the data directory."""
        candidates = []
        
        if not self.data_dir.exists():
            return candidates
        
        for file_path in self.data_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.docx', '.txt']:
                candidate_data = self.parse_candidate_document(str(file_path))
                if candidate_data['content']:
                    candidates.append(candidate_data)
        
        return candidates
    
    def load_job_description(self, job_file: str) -> str:
        """Load job description from file."""
        job_path = Path("data/job_descriptions") / job_file
        if job_path.exists():
            return self.load_text(str(job_path))
        return ""
