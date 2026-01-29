"""
Memory and Analytics API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.agents.memory_agent import MemoryAgent
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/memory", tags=["memory"])

memory_agent = MemoryAgent()


@router.get("/health")
async def health_check():
    """Health check for memory service"""
    return {"status": "healthy", "service": "memory"}


@router.get("/{user_id}/summary")
async def get_memory_summary(user_id: int, current_user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    """Get user memory summary"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        summary = memory_agent.get_memory_summary(db, user_id)
        return {
            "success": True,
            "data": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching memory summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch memory summary")


@router.get("/{user_id}/strengths")
async def get_strengths(user_id: int, limit: int = 10,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """Get user strengths"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        strengths = memory_agent.get_strengths(db, user_id, limit)
        return {
            "success": True,
            "strengths": strengths,
            "count": len(strengths)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching strengths: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch strengths")


@router.get("/{user_id}/weaknesses")
async def get_weaknesses(user_id: int, limit: int = 10,
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """Get user weaknesses"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        weaknesses = memory_agent.get_weaknesses(db, user_id, limit)
        return {
            "success": True,
            "weaknesses": weaknesses,
            "count": len(weaknesses)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching weaknesses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch weaknesses")


@router.get("/{user_id}/covered-topics")
async def get_covered_topics(user_id: int, limit: int = 15,
                            current_user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    """Get covered topics"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        topics = memory_agent.get_covered_topics(db, user_id, limit)
        return {
            "success": True,
            "topics": topics,
            "count": len(topics)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching covered topics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch covered topics")


@router.get("/{user_id}/missed-topics")
async def get_missed_topics(user_id: int, limit: int = 15,
                           current_user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    """Get missed topics to focus on"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        topics = memory_agent.get_missed_topics(db, user_id, limit)
        return {
            "success": True,
            "topics": topics,
            "count": len(topics)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching missed topics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch missed topics")


@router.post("/{user_id}/store-strength")
async def store_strength(user_id: int, strength_data: Dict[str, Any],
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """Store strength area"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        strength_area = strength_data.get("area", "")
        score = strength_data.get("score", 8.0)
        metadata = strength_data.get("metadata", {})
        
        if not strength_area:
            raise HTTPException(status_code=400, detail="Strength area required")
        
        memory_agent.store_strength(db, user_id, strength_area, score, metadata)
        logger.info(f"Strength stored for user {user_id}: {strength_area}")
        return {"success": True, "message": "Strength stored successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing strength: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store strength")


@router.post("/{user_id}/store-weakness")
async def store_weakness(user_id: int, weakness_data: Dict[str, Any],
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """Store weakness area"""
    try:
        if current_user.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        weakness_area = weakness_data.get("area", "")
        improvement_steps = weakness_data.get("improvement_steps", [])
        metadata = weakness_data.get("metadata", {})
        
        if not weakness_area:
            raise HTTPException(status_code=400, detail="Weakness area required")
        
        memory_agent.store_weakness(db, user_id, weakness_area, improvement_steps, metadata)
        logger.info(f"Weakness stored for user {user_id}: {weakness_area}")
        return {"success": True, "message": "Weakness stored successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing weakness: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store weakness")

