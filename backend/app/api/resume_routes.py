"""
Resume API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from app.services.resume_service import ResumeService
from app.schemas.schemas import ResumeAnalysisResponse
from app.utils.security import get_current_user
from app.utils.logging_config import get_logger
from app.utils.exceptions import ValidationError

logger = get_logger(__name__)
router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    target_company: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and analyze a resume against a job role and company.
    """
    try:
        # Validate file size (e.g., 5MB limit)
        file_content = await file.read()
        if len(file_content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max size is 5MB.")
            
        analysis = await ResumeService.analyze_resume(
            file_content=file_content,
            filename=file.filename,
            target_role=target_role,
            target_company=target_company
        )
        
        return analysis
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in resume analysis route: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze resume")
