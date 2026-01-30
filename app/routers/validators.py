from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from app.uploads.cvs.validators import DocumentValidator
from app.routers import ai

# Create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/validators", tags=["validators"])

doc_validator = DocumentValidator(max_size=5 * 1024 * 1024)  # 5MB limit

@router.post("/upload/single")
async def upload_single_file(file: UploadFile = File(...)):
    """Upload a single file with basic validation"""
    # Validate the file first
    validation = await doc_validator.validate_file(file)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "File validation failed",
                "errors": validation["errors"]
            }
        )
    
    # Create unique filename to prevent conflicts
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    return {
        "success": True,
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "size": file.size,
        "upload_time": datetime.utcnow().isoformat(),
        "location": str(file_path)
    }


@router.get("/")
async def root():
    return {"message": "FastAPI File Upload Service is running"}
