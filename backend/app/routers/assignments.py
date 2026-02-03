from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.assignment import Assignment
from app.models.quest import Quest
from app.models.zone import Zone
from app.models.world import World
from app.models.teacher import Teacher
from app.models.user import User
from app.models.submission import Submission
from app.models.notification import Notification
from app.schemas.assignment import AssignmentCreate, AssignmentResponse, AssignmentUpdate
from app.utils.dependencies import get_current_teacher, get_current_user

router = APIRouter(prefix="/api/assignments", tags=["Assignments (Bounties)"])


@router.get("/teacher/all")
async def get_teacher_assignments(
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all assignments created by the current teacher (across all their worlds).
    """
    # Get all worlds owned by this teacher
    teacher_worlds = db.query(World).filter(World.teacher_id == current_teacher.teacher_id).all()
    
    if not teacher_worlds:
        return []
    
    world_ids = [w.world_id for w in teacher_worlds]
    
    # Get all zones in these worlds
    zones = db.query(Zone).filter(Zone.world_id.in_(world_ids)).all()
    
    if not zones:
        return []
    
    zone_ids = [z.zone_id for z in zones]
    
    # Get all quests in these zones
    quests = db.query(Quest).filter(Quest.zone_id.in_(zone_ids)).all()
    
    if not quests:
        return []
    
    quest_ids = [q.quest_id for q in quests]
    
    # Get all assignments for these quests
    assignments = db.query(Assignment).filter(Assignment.quest_id.in_(quest_ids)).order_by(desc(Assignment.created_at)).all()
    
    # Return as plain dict for frontend
    return [{
        "assignment_id": a.assignment_id,
        "quest_id": a.quest_id,
        "title": a.title,
        "description": a.description,
        "max_score": a.max_score,
        "xp_reward": a.xp_reward,
        "gold_reward": a.gold_reward,
        "due_date": a.due_date.isoformat() if a.due_date else None,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    } for a in assignments]


@router.get("/user/pending")
async def get_user_pending_assignments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all pending (not yet submitted or graded) assignments for the current user.
    Returns assignments with due dates and submission status.
    """
    # Get all published worlds relevant to the user's class (World-Level Permission)
    published_worlds = db.query(World).filter(
        World.is_published == True,
        or_(
            World.required_class == "All",
            World.required_class == None,
            World.required_class == current_user.avatar_class
        )
    ).all()
    
    if not published_worlds:
        return []
    
    world_ids = [w.world_id for w in published_worlds]
    
    # Get all zones
    zones = db.query(Zone).filter(Zone.world_id.in_(world_ids)).all()
    
    if not zones:
        return []
    
    zone_ids = [z.zone_id for z in zones]
    
    # Get all quests
    quests = db.query(Quest).filter(Quest.zone_id.in_(zone_ids)).all()
    
    if not quests:
        return []
    
    quest_ids = [q.quest_id for q in quests]
    
    # Get all assignments with upcoming or no due date
    # AND filter by Assignment-Level Class Restriction
    all_assignments = db.query(Assignment).filter(
        Assignment.quest_id.in_(quest_ids),
        or_(
            Assignment.required_class == "All",
            Assignment.required_class == None,
            Assignment.required_class == current_user.avatar_class
        )
    ).all()
    
    # Check submission status for each
    result = []
    for assignment in all_assignments:
        submission = db.query(Submission).filter(
            Submission.assignment_id == assignment.assignment_id,
            Submission.user_id == current_user.user_id
        ).first()
        
        # Determine status
        if submission:
            if submission.status == 'approved':
                status = 'completed'
            elif submission.status == 'rejected':
                status = 'rejected'
            else:
                status = 'pending_review'
        else:
            status = 'not_submitted'
        
        # Get quest and world info
        quest = db.query(Quest).filter(Quest.quest_id == assignment.quest_id).first()
        zone = db.query(Zone).filter(Zone.zone_id == quest.zone_id).first() if quest else None
        world = db.query(World).filter(World.world_id == zone.world_id).first() if zone else None
        
        result.append({
            "assignment_id": assignment.assignment_id,
            "title": assignment.title,
            "description": assignment.description,
            "max_score": assignment.max_score,
            "xp_reward": assignment.xp_reward,
            "gold_reward": assignment.gold_reward,
            "due_date": assignment.due_date,
            "status": status,
            "quest_title": quest.title if quest else None,
            "world_title": world.title if world else None,
            "is_overdue": assignment.due_date and assignment.due_date < datetime.now() and status == 'not_submitted'
        })
    
    # Sort by due date (upcoming first, then no due date)
    result.sort(key=lambda x: (x['due_date'] is None, x['due_date'] or datetime.max))
    
    return result


@router.get("/quest/{quest_id}", response_model=List[AssignmentResponse])
async def get_assignments_by_quest(
    quest_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all assignments for a specific quest.
    """
    assignments = db.query(Assignment).filter(Assignment.quest_id == quest_id).all()
    return assignments


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get an assignment by ID.
    """
    assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return assignment


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new assignment (teacher only).
    """
    quest = db.query(Quest).filter(Quest.quest_id == assignment_data.quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    # Note: Ownership check removed - any teacher can create assignments in any world
    # This allows for collaborative course management
    
    new_assignment = Assignment(
        quest_id=assignment_data.quest_id,
        title=assignment_data.title,
        description=assignment_data.description,
        max_score=assignment_data.max_score,
        xp_reward=assignment_data.xp_reward,
        gold_reward=assignment_data.gold_reward,
        due_date=assignment_data.due_date,
        required_class=assignment_data.required_class
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    # Create notifications for eligible users
    # Get the world info for context
    zone = quest.zone
    world = zone.world if zone else None
    world_title = world.title if world else "Unknown World"
    world_class = world.required_class if world else "All"
    assignment_class = assignment_data.required_class or "All"
    
    # Determine which users should be notified based on class restrictions
    if assignment_class == "All" and world_class == "All":
        # Notify all users
        eligible_users = db.query(User).all()
    elif assignment_class != "All":
        # Notify users of the specific assignment class
        eligible_users = db.query(User).filter(User.avatar_class == assignment_class).all()
    elif world_class != "All":
        # Notify users of the world's class
        eligible_users = db.query(User).filter(User.avatar_class == world_class).all()
    else:
        eligible_users = db.query(User).all()
    
    # Create notification for each eligible user
    for user in eligible_users:
        notification = Notification(
            user_id=user.user_id,
            title="📝 New Assignment Available!",
            message=f"'{new_assignment.title}' has been posted in {world_title}. Complete it to earn {new_assignment.xp_reward} XP!",
            icon="📝",
            notification_type="assignment",
            related_id=new_assignment.assignment_id,
            related_type="assignment"
        )
        db.add(notification)
    
    db.commit()
    
    return new_assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update an assignment (teacher only).
    """
    assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Note: Ownership check removed - any teacher can edit assignments
    
    if assignment_update.title is not None:
        assignment.title = assignment_update.title
    if assignment_update.description is not None:
        assignment.description = assignment_update.description
    if assignment_update.max_score is not None:
        assignment.max_score = assignment_update.max_score
    if assignment_update.xp_reward is not None:
        assignment.xp_reward = assignment_update.xp_reward
    if assignment_update.gold_reward is not None:
        assignment.gold_reward = assignment_update.gold_reward
    if assignment_update.due_date is not None:
        assignment.due_date = assignment_update.due_date
    if assignment_update.required_class is not None:
        assignment.required_class = assignment_update.required_class
    
    db.commit()
    db.refresh(assignment)
    
    return assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Delete an assignment (teacher only).
    """
    assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Note: Ownership check removed - any teacher can delete assignments
    
    db.delete(assignment)
    db.commit()
    
    return None
