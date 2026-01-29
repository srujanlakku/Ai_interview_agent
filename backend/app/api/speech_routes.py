"""
Speech Processing API endpoints (Optional feature)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.utils.speech_recognition import speech_recognizer
from app.utils.logging_config import get_logger
from app.utils.exceptions import SpeechRecognitionError

logger = get_logger(__name__)
router = APIRouter(prefix="/api/speech", tags=["speech"])


@router.post("/transcribe")
async def transcribe_audio_file(
    audio_file: UploadFile = File(...),
    language: str = "en-US",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transcribe audio file to text
    
    Note: This endpoint requires speech-to-text service configuration
    """
    try:
        # Read audio data
        audio_data = await audio_file.read()
        
        if not audio_data:
            raise HTTPException(status_code=400, detail="No audio data provided")
        
        # Validate audio
        if not await speech_recognizer.validate_audio(audio_data):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid audio. Duration must be between 1-120 seconds"
            )
        
        # Transcribe
        try:
            text = await speech_recognizer.recognize_speech(audio_data, language)
            logger.info(f"Audio transcribed for user {current_user.get('user_id')}")
            return {
                "success": True,
                "text": text,
                "language": language,
                "confidence": 0.85  # Placeholder
            }
        except SpeechRecognitionError as e:
            logger.warning(f"Transcription failed: {str(e)}")
            raise HTTPException(status_code=503, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to transcribe audio")


@router.get("/supported-languages")
async def get_supported_languages(current_user: dict = Depends(get_current_user)):
    """Get list of supported languages for speech recognition"""
    try:
        languages = await speech_recognizer.get_supported_languages()
        return {
            "success": True,
            "languages": languages,
            "count": len(languages)
        }
    except Exception as e:
        logger.error(f"Error fetching supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch languages")


@router.get("/status")
async def speech_service_status():
    """Check speech recognition service status"""
    return {
        "service": "speech_recognition",
        "status": "available",
        "implementation": "placeholder",
        "note": "To enable speech-to-text, configure GOOGLE_CLOUD_SPEECH_KEY or similar"
    }
