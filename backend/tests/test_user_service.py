"""
Tests for user service
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, User
from app.services.user_service import UserService
from app.schemas.schemas import UserCreate, UserProfileCreate
from app.utils.exceptions import DuplicateError, AuthenticationError, NotFoundError

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user_success(db):
    """Test successful user creation"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    user = UserService.create_user(db, user_create)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"


def test_create_user_duplicate(db):
    """Test duplicate user creation"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    UserService.create_user(db, user_create)
    
    with pytest.raises(DuplicateError):
        UserService.create_user(db, user_create)


def test_authenticate_user_success(db):
    """Test successful authentication"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    UserService.create_user(db, user_create)
    
    user = UserService.authenticate_user(db, "test@example.com", "Password123")
    assert user.email == "test@example.com"


def test_authenticate_user_invalid_password(db):
    """Test authentication with invalid password"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    UserService.create_user(db, user_create)
    
    with pytest.raises(AuthenticationError):
        UserService.authenticate_user(db, "test@example.com", "WrongPassword")


def test_get_user_by_id(db):
    """Test getting user by ID"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    created_user = UserService.create_user(db, user_create)
    
    user = UserService.get_user_by_id(db, created_user.id)
    assert user.id == created_user.id


def test_get_user_not_found(db):
    """Test getting non-existent user"""
    with pytest.raises(NotFoundError):
        UserService.get_user_by_id(db, 99999)


def test_create_user_profile(db):
    """Test user profile creation"""
    user_create = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Password123"
    )
    user = UserService.create_user(db, user_create)
    
    profile_create = UserProfileCreate(
        target_company="Google",
        target_role="Software Engineer",
        interview_type="Technical",
        experience_level="Mid",
        available_hours=20
    )
    
    profile = UserService.create_user_profile(db, user.id, profile_create)
    assert profile.target_company == "Google"
    assert profile.target_role == "Software Engineer"
