from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherResponse, TeacherUpdate
from app.utils.dependencies import get_current_teacher

router = APIRouter(prefix="/api/teachers", tags=["Teachers (Guild Masters)"])


@router.get("/me", response_model=TeacherResponse)
async def get_current_teacher_profile(current_teacher: Teacher = Depends(get_current_teacher)):
    """
    Get the current authenticated teacher's profile.
    """
    return current_teacher


@router.put("/me", response_model=TeacherResponse)
async def update_current_teacher_profile(
    teacher_update: TeacherUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update the current teacher's profile.
    """
    if teacher_update.username:
        existing = db.query(Teacher).filter(
            Teacher.username == teacher_update.username,
            Teacher.teacher_id != current_teacher.teacher_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_teacher.username = teacher_update.username
    
    if teacher_update.email:
        existing = db.query(Teacher).filter(
            Teacher.email == teacher_update.email,
            Teacher.teacher_id != current_teacher.teacher_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_teacher.email = teacher_update.email
    
    if teacher_update.bio is not None:
        current_teacher.bio = teacher_update.bio
    
    if teacher_update.specialization is not None:
        current_teacher.specialization = teacher_update.specialization
    
    db.commit()
    db.refresh(current_teacher)
    
    return current_teacher


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_by_id(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a teacher's public profile by ID.
    """
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return teacher
