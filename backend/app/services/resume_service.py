"""
Resume Service - Handles resume file parsing and analysis coordination.
"""
import io
import PyPDF2
import docx
from typing import Dict, Any, Optional
from app.agents.resume_analyzer_agent import ResumeAnalyzerAgent
from app.utils.logging_config import get_logger
from app.utils.exceptions import ValidationError

logger = get_logger(__name__)
resume_agent = ResumeAnalyzerAgent()

class ResumeService:
    """Service for handling resume processing and analysis"""

    @staticmethod
    def parse_pdf(file_content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise ValidationError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def parse_docx(file_content: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            raise ValidationError(f"Failed to parse DOCX: {str(e)}")

    @staticmethod
    async def analyze_resume(
        file_content: bytes, 
        filename: str, 
        target_role: str, 
        target_company: Optional[str] = None
    ) -> Dict[str, Any]:
        """Parse and analyze resume"""
        
        # 1. Parse file based on extension
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            text = ResumeService.parse_pdf(file_content)
        elif ext == 'docx':
            text = ResumeService.parse_docx(file_content)
        else:
            raise ValidationError(f"Unsupported file format: {ext}. Only PDF and DOCX are allowed.")

        if not text.strip():
            raise ValidationError("Resume file appears to be empty or unreadable.")

        # 2. Call Agent for analysis
        logger.info(f"Analyzing resume {filename} for role {target_role}")
        analysis = await resume_agent.execute(
            resume_text=text[:8000], # Basic truncation to avoid LLM token limits
            target_role=target_role,
            target_company=target_company or "General"
        )

        return analysis
