from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.teacher import Teacher
from app.services.auth_service import AuthService
from app.schemas.auth import TokenData

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    """
    token_data: TokenData = AuthService.decode_token(token)
    
    if token_data.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required"
        )
    
    user = db.query(User).filter(User.user_id == token_data.id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def get_current_teacher(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Teacher:
    """
    Dependency to get the current authenticated teacher.
    """
    token_data: TokenData = AuthService.decode_token(token)
    
    if token_data.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )
    
    teacher = db.query(Teacher).filter(Teacher.teacher_id == token_data.id).first()
    
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return teacher


async def get_current_user_or_teacher(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency to get either current user or teacher.
    """
    token_data: TokenData = AuthService.decode_token(token)
    
    if token_data.role == "user":
        user = db.query(User).filter(User.user_id == token_data.id).first()
        if user:
            return {"type": "user", "entity": user}
    elif token_data.role == "teacher":
        teacher = db.query(Teacher).filter(Teacher.teacher_id == token_data.id).first()
        if teacher:
            return {"type": "teacher", "entity": teacher}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Account not found"
    )
