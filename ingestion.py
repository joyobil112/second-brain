import os
from pathlib import Path
from pypdf import PdfReader
import config

class DocumentParser:
    """Handles the detection and extraction of text from various file formats."""
    
    @staticmethod
    def parse_txt(file_path: Path) -> str:
        """Extracts text from a plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    @staticmethod
    def parse_pdf(file_path: Path) -> str:
        """Extracts text from a PDF file natively using pypdf."""
        reader = PdfReader(file_path)
        extracted_text = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
                
        return "\n".join(extracted_text).strip()

    def scan_inbox(self) -> list[dict]:
        """Scans the inbox directory for unprocessed documents."""
        supported_extensions = {'.txt', '.pdf'}
        processed_documents = []
        
        # Grab all files in the inbox folder
        for file in config.INBOX_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in supported_extensions:
                print(f"🔄 Found file for ingestion: {file.name}")
                
                try:
                    if file.suffix.lower() == '.txt':
                        text = self.parse_txt(file)
                    elif file.suffix.lower() == '.pdf':
                        text = self.parse_pdf(file)
                    
                    if text:
                        processed_documents.append({
                            "filename": file.name,
                            "original_path": file,
                            "content": text
                        })
                    else:
                        print(f"⚠️ Warning: No text extracted from {file.name}")
                        
                except Exception as e:
                    print(f"❌ Error parsing {file.name}: {str(e)}")
                    
        return processed_documents