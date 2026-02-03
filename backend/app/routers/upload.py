from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import secrets
from pathlib import Path

router = APIRouter(prefix="/api/upload", tags=["Upload"])

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

from app.utils.dependencies import get_current_user
from app.models.user import User
from fastapi import Depends

@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    # current_user: User = Depends(get_current_user) # Auth removed by user request
):
    try:
        # Generate a unique filename to prevent overwrites
        file_ext = os.path.splitext(file.filename)[1]
        random_name = secrets.token_hex(8)
        filename = f"{random_name}{file_ext}"
        
        file_path = UPLOAD_DIR / filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return the URL (relative path that will be served by StaticFiles)
        url = f"/static/uploads/{filename}"
        
        return {"url": url, "filename": filename}
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Could not upload file")
