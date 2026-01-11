"""
Media Upload and Processing API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import os
from pathlib import Path

from database import get_db
from db import models
import schemas
from storage import StorageService
from celery_app import process_media_task

router = APIRouter()
storage_service = StorageService()


@router.post("/upload", response_model=schemas.MediaUpload, status_code=status.HTTP_201_CREATED)
async def upload_media(
    file: UploadFile = File(...),
    camera_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload video or image for processing
    """
    # Validate camera exists
    camera = db.query(models.Camera).filter(models.Camera.id == UUID(camera_id)).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
        file_type = 'video'
    elif file_ext in ['.jpg', '.jpeg', '.png']:
        file_type = 'image'
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type"
        )
    
    # Upload to storage
    try:
        file_url = await storage_service.upload_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
    
    # Create database record
    media_upload = models.MediaUpload(
        camera_id=UUID(camera_id),
        file_name=file.filename,
        file_type=file_type,
        file_url=file_url,
        processing_status="pending"
    )
    db.add(media_upload)
    db.commit()
    db.refresh(media_upload)
    
    # Trigger async processing
    process_media_task.delay(str(media_upload.id))
    
    return media_upload


@router.get("/{media_id}", response_model=schemas.MediaUpload)
def get_media_status(
    media_id: UUID,
    db: Session = Depends(get_db)
):
    """Get media upload status and details"""
    media = db.query(models.MediaUpload).filter(models.MediaUpload.id == media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return media


@router.get("/{media_id}/detections", response_model=list[schemas.Detection])
def get_media_detections(
    media_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all detections for a media upload"""
    media = db.query(models.MediaUpload).filter(models.MediaUpload.id == media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    detections = db.query(models.Detection).filter(models.Detection.media_id == media_id).all()
    return detections