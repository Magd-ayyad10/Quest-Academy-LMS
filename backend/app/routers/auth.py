from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.models.teacher import Teacher
from app.schemas.user import UserCreate, UserResponse
from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.schemas.auth import Token, LoginRequest
from app.services.auth_service import AuthService
from app.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
settings = get_settings()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (hero).
    """
    # Check if email already exists
    if AuthService.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = AuthService.get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        avatar_class=user_data.avatar_class or "Novice"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login a user and return a JWT token.
    Uses OAuth2 form (username field contains email).
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(
        data={
            "sub": str(user.user_id),
            "username": user.username,
            "role": "user"
        }
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/teacher/register", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def register_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db)):
    """
    Register a new teacher (guild master).
    """
    # Check if email already exists
    if AuthService.get_teacher_by_email(db, teacher_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_teacher = db.query(Teacher).filter(Teacher.username == teacher_data.username).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new teacher
    hashed_password = AuthService.get_password_hash(teacher_data.password)
    new_teacher = Teacher(
        username=teacher_data.username,
        email=teacher_data.email,
        password_hash=hashed_password,
        bio=teacher_data.bio,
        specialization=teacher_data.specialization
    )
    
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    
    return new_teacher


@router.post("/teacher/login", response_model=Token)
async def login_teacher(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login a teacher and return a JWT token.
    """
    teacher = AuthService.authenticate_teacher(db, form_data.username, form_data.password)
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(
        data={
            "sub": str(teacher.teacher_id),
            "username": teacher.username,
            "role": "teacher"
        }
    )
    
    return Token(access_token=access_token, token_type="bearer")
