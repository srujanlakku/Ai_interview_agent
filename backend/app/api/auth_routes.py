"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.utils.database import get_db
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.utils.security import create_access_token, decode_token, get_current_user
from app.utils.exceptions import DuplicateError, AuthenticationError, ValidationError
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse)
async def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    try:
        user = UserService.create_user(db, user_create)
        logger.info(f"User signed up: {user.email}")
        return user
    except DuplicateError as e:
        logger.warning(f"Signup failed - duplicate user: {str(e)}")
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        logger.warning(f"Signup failed - validation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    try:
        user = UserService.authenticate_user(db, user_login.email, user_login.password)
        access_token = create_access_token({"sub": user.email, "user_id": user.id})
        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthenticationError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (token becomes invalid on client side)"""
    try:
        logger.info(f"User logged out: {current_user.get('sub')}")
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user profile"""
    try:
        email = current_user.get("sub")
        user = UserService.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")



