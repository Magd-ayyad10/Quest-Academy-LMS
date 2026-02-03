from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.submission import Submission, SubmissionStatus
from app.models.assignment import Assignment
from app.models.user import User
from app.models.teacher import Teacher
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionGrade
from app.utils.dependencies import get_current_user, get_current_teacher
from app.services.game_service import GameService

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])


@router.get("/my", response_model=List[SubmissionResponse])
async def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all submissions for the current user.
    """
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.user_id
    ).all()
    return submissions


@router.get("/assignment/{assignment_id}", response_model=List[SubmissionResponse])
async def get_submissions_for_assignment(
    assignment_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all submissions for an assignment (teacher only).
    """
    assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view these submissions"
        )
    
    submissions = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).all()
    
    return submissions


@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission_data: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit work for an assignment.
    """
    print(f"DEBUG: Processing submission for user {current_user.username}")
    print(f"DEBUG: Data: {submission_data}")
    
    assignment = db.query(Assignment).filter(
        Assignment.assignment_id == submission_data.assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check for existing submission
    existing = db.query(Submission).filter(
        Submission.assignment_id == submission_data.assignment_id,
        Submission.user_id == current_user.user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted for this assignment"
        )
    
    new_submission = Submission(
        assignment_id=submission_data.assignment_id,
        user_id=current_user.user_id,
        submission_url=submission_data.submission_url,
        submission_text=submission_data.submission_text,
        status=SubmissionStatus.PENDING
    )
    
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    
    # === AI AUTO-GRADING ===
    try:
        from app.services.ai_grader import AIGraderService
        from app.models.ai_grading import AIGradingLog
        
        # Determine content to grade
        content_to_grade = submission_data.submission_text or "See attached file."
        
        grading_result = await AIGraderService.grade_submission(
            assignment_title=assignment.title,
            assignment_description=assignment.description,
            submission_text=content_to_grade,
            submission_url=submission_data.submission_url
        )
        
        # Apply Grading
        new_submission.grade_awarded = grading_result.get("score", 0)
        new_submission.teacher_feedback = grading_result.get("feedback", "Pending review.")
        
        status_str = grading_result.get("status", "pending")
        if status_str == "approved":
            new_submission.status = SubmissionStatus.APPROVED
        elif status_str == "rejected":
            new_submission.status = SubmissionStatus.REJECTED
        else:
            new_submission.status = SubmissionStatus.PENDING
            
        new_submission.graded_at = datetime.utcnow()
        
        # Award Rewards if Approved
        if new_submission.status == SubmissionStatus.APPROVED:
            # Calculate proportional rewards
            grade_percent = new_submission.grade_awarded / assignment.max_score
            xp_earned = int(assignment.xp_reward * grade_percent)
            gold_earned = int(assignment.gold_reward * grade_percent)
            
            if xp_earned > 0:
                GameService.award_xp(db, current_user, xp_earned)
            if gold_earned > 0:
                GameService.award_gold(db, current_user, gold_earned)
                
            # Update Weekly Progress
            GameService.update_weekly_progress(db, current_user.user_id, xp_earned, activity_type="quest_complete") 
                
        # === Log to AIGradingLog Table ===
        try:
            ai_log = AIGradingLog(
                submission_id=new_submission.submission_id,
                assignment_id=assignment.assignment_id,
                user_id=current_user.user_id,
                user_email=current_user.email,
                score_awarded=new_submission.grade_awarded or 0,
                feedback_text=new_submission.teacher_feedback,
                status_verdict=status_str
            )
            db.add(ai_log)
        except Exception as log_err:
            print(f"ERROR: Failed to create AI log: {log_err}")
            import traceback
            traceback.print_exc()

        db.commit()
    except Exception as e:
        db.rollback() # Rollback potentially failed transaction state from AI logic
        print(f"ERROR inside AI Grading Block: {e}")
        import traceback
        traceback.print_exc()
        # Ensure the basic submission is still saved!
        # The first commit happened at line 105, so the submission exists.
        # We just need to ensure we don't leave the DB in an invalid state if something exploded.
        pass
    
    db.refresh(new_submission)
    
    return new_submission


@router.put("/{submission_id}/grade", response_model=SubmissionResponse)
async def grade_submission(
    submission_id: int,
    grade_data: SubmissionGrade,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Grade a submission (teacher only).
    """
    submission = db.query(Submission).filter(
        Submission.submission_id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    assignment = submission.assignment
    if assignment.quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to grade this submission"
        )
    
    # Update submission
    submission.status = SubmissionStatus(grade_data.status.value)
    submission.grade_awarded = grade_data.grade_awarded
    submission.teacher_feedback = grade_data.teacher_feedback
    submission.graded_at = datetime.utcnow()
    
    # Award XP and gold if approved
    if grade_data.status == SubmissionStatus.APPROVED:
        user = submission.user
        
        # Calculate rewards based on grade percentage
        grade_percent = grade_data.grade_awarded / assignment.max_score
        xp_earned = int(assignment.xp_reward * grade_percent)
        gold_earned = int(assignment.gold_reward * grade_percent)
        
        if xp_earned > 0:
            GameService.award_xp(db, user, xp_earned)
        if gold_earned > 0:
            GameService.award_gold(db, user, gold_earned)
    
    db.commit()
    db.refresh(submission)
    
    return submission
