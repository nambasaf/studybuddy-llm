import PyPDF2
import re
from typing import List

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 500 # tokens
        self.overlap = 50 # token overlap between chunks

    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF"""
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean text and normalize it"""
        # Collapse extra spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove ONLY weird non-text symbols (keep words and punctuation)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:-]', '', text)
        return text.strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)

            if i + self.chunk_size >= len(words):
                break
        return chunks
    
    def process_document(self, pdf_file):
        """Main processing pipeline"""
        # Extract the text
        raw_text = self.extract_text_from_pdf(pdf_file)
        

        # clean the text
        clean_text = self.clean_text(raw_text)
        # create chunks
        chunks = self.chunk_text(clean_text)
        return chunks
        
