"""
User Profile and Onboarding API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.schemas import UserProfileCreate, UserProfileResponse
from app.services.user_service import UserService
from app.agents.research_agent import ResearchAgent
from app.agents.learning_agent import LearningAgent
from app.utils.security import get_current_user
from app.utils.logging_config import get_logger
from app.utils.exceptions import NotFoundError, ValidationError
import asyncio

logger = get_logger(__name__)
router = APIRouter(prefix="/api/profile", tags=["profile"])

research_agent = ResearchAgent()
learning_agent = LearningAgent()


@router.post("/onboard", response_model=UserProfileResponse)
async def onboard_user(
    profile_create: UserProfileCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Onboard user with profile information"""
    try:
        user_id = current_user.get("user_id")
        profile = UserService.create_user_profile(db, user_id, profile_create)
        logger.info(f"User onboarded: {user_id}")
        
        # Trigger research and learning material generation
        asyncio.create_task(generate_preparation_materials(profile_create, db))
        
        return profile
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error onboarding user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to onboard user")


@router.get("/get", response_model=UserProfileResponse)
async def get_user_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get current user profile"""
    try:
        user_id = current_user.get("user_id")
        profile = UserService.get_user_profile(db, user_id)
        return profile
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")


@router.post("/prepare")
async def generate_preparation(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Generate preparation materials for current user"""
    try:
        user_id = current_user.get("user_id")
        profile = UserService.get_user_profile(db, user_id)
        
        # Research company patterns
        research_result = await research_agent.execute(
            profile.target_company,
            profile.target_role
        )
        
        if not research_result.get("success"):
            logger.warning(f"Research failed for {profile.target_company}")
            research_data = {
                "required_skills": [],
                "technologies": [],
                "frequently_asked_questions": []
            }
        else:
            research_data = research_result.get("data", {})
        
        # Generate learning materials
        user_profile_dict = {
            "experience_level": profile.experience_level,
            "available_hours": profile.available_hours
        }
        
        learning_result = await learning_agent.execute(user_profile_dict, research_data)
        
        return {
            "success": True,
            "research": research_data,
            "learning_materials": learning_result.get("materials", []),
            "total_materials": learning_result.get("total_materials", 0)
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating preparation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate preparation")


async def generate_preparation_materials(profile_create: UserProfileCreate, db: Session):
    """Background task to generate preparation materials"""
    try:
        result = await research_agent.execute(
            profile_create.target_company,
            profile_create.target_role
        )
        logger.info(f"Preparation materials generated for {profile_create.target_company}")
    except Exception as e:
        logger.error(f"Error generating preparation materials: {str(e)}")
