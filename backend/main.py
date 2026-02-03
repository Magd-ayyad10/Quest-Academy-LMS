from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import (
    auth,
    users,
    teachers,
    worlds,
    zones,
    quests,
    monsters,
    assignments,
    submissions,
    progress,
    inventory,
    achievements,
    leaderboard,
    battle,
    engagement,
    admin,
    upload,
    notifications
)
from fastapi.staticfiles import StaticFiles
import os

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)


settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="""
    🎮 **Quest Academy LMS API**
    
    A gamified Learning Management System with an RPG theme.
    
    ## Features
    
    - **Heroes (Users)**: Students with RPG stats (Level, XP, HP, Gold)
    - **Guild Masters (Teachers)**: Create and manage courses
    - **Worlds (Courses)**: Learning worlds to explore
    - **Zones (Modules)**: Areas within worlds
    - **Quests (Lessons)**: Learning content with rewards
    - **Monsters (Quizzes)**: Auto-graded challenges
    - **Bounties (Assignments)**: Manual tasks with grading
    - **Inventory & Shop**: Items with stat bonuses
    - **Achievements**: Unlockable trophies
    - **Leaderboard**: Compete with other heroes
    
    ## Authentication
    
    Most endpoints require JWT authentication. Use the `/api/auth/login` endpoint to get a token.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(teachers.router)
app.include_router(worlds.router)
app.include_router(zones.router)
app.include_router(quests.router)
app.include_router(monsters.router)
app.include_router(assignments.router)
app.include_router(submissions.router)
app.include_router(progress.router)
app.include_router(inventory.router)
app.include_router(achievements.router)
app.include_router(leaderboard.router)
app.include_router(battle.router)
app.include_router(engagement.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(notifications.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "⚔️ Welcome to Quest Academy LMS!",
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
