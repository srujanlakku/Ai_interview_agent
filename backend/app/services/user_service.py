"""
User service for handling user operations
"""
from sqlalchemy.orm import Session
from app.models.database import User, UserProfile
from app.schemas.schemas import UserCreate, UserProfileCreate
from app.utils.security import hash_password, verify_password
from app.utils.exceptions import DuplicateError, AuthenticationError, NotFoundError, ValidationError
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for user management"""

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_create.email).first()
            if existing_user:
                logger.warning(f"Attempt to create duplicate user: {user_create.email}")
                raise DuplicateError(f"User with email {user_create.email} already exists")

            # Create new user
            hashed_password = hash_password(user_create.password)
            db_user = User(
                email=user_create.email,
                full_name=user_create.full_name,
                hashed_password=hashed_password
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created successfully: {user_create.email}")
            return db_user
        except DuplicateError:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise ValidationError(f"Failed to create user: {str(e)}")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                logger.warning(f"Login attempt with non-existent email: {email}")
                raise AuthenticationError("Invalid email or password")

            if not verify_password(password, user.hashed_password):
                logger.warning(f"Failed login attempt for user: {email}")
                raise AuthenticationError("Invalid email or password")

            if not user.is_active:
                logger.warning(f"Login attempt by inactive user: {email}")
                raise AuthenticationError("User account is inactive")

            logger.info(f"User authenticated successfully: {email}")
            return user
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            raise AuthenticationError("Authentication failed")

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError(f"User with ID {user_id} not found")
            return user
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            raise NotFoundError("User not found")

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise NotFoundError(f"User with email {email} not found")
            return user
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            raise NotFoundError("User not found")

    @staticmethod
    def create_user_profile(db: Session, user_id: int, profile_create: UserProfileCreate) -> UserProfile:
        """Create or update user profile"""
        try:
            # Check if user exists
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError(f"User with ID {user_id} not found")

            # Check if profile already exists
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile:
                # Update existing profile
                profile.target_company = profile_create.target_company
                profile.target_role = profile_create.target_role
                profile.interview_type = profile_create.interview_type
                profile.experience_level = profile_create.experience_level
                profile.available_hours = profile_create.available_hours
            else:
                # Create new profile
                profile = UserProfile(
                    user_id=user_id,
                    target_company=profile_create.target_company,
                    target_role=profile_create.target_role,
                    interview_type=profile_create.interview_type,
                    experience_level=profile_create.experience_level,
                    available_hours=profile_create.available_hours
                )
                db.add(profile)

            db.commit()
            db.refresh(profile)
            logger.info(f"User profile created/updated for user {user_id}")
            return profile
        except NotFoundError:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user profile: {str(e)}")
            raise ValidationError(f"Failed to create profile: {str(e)}")

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> UserProfile:
        """Get user profile"""
        try:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if not profile:
                raise NotFoundError(f"Profile for user {user_id} not found")
            return profile
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user profile: {str(e)}")
            raise NotFoundError("Profile not found")
