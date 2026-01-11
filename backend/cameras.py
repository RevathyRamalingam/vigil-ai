"""
Camera Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.db import models
from app.schemas import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Camera])
def list_cameras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all cameras"""
    cameras = db.query(models.Camera).offset(skip).limit(limit).all()
    return cameras


@router.post("/", response_model=schemas.Camera, status_code=status.HTTP_201_CREATED)
def create_camera(
    camera: schemas.CameraCreate,
    db: Session = Depends(get_db)
):
    """Register a new camera"""
    db_camera = models.Camera(**camera.dict())
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


@router.get("/{camera_id}", response_model=schemas.Camera)
def get_camera(
    camera_id: UUID,
    db: Session = Depends(get_db)
):
    """Get camera details by ID"""
    camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    return camera


@router.put("/{camera_id}", response_model=schemas.Camera)
def update_camera(
    camera_id: UUID,
    camera_update: schemas.CameraUpdate,
    db: Session = Depends(get_db)
):
    """Update camera information"""
    camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    update_data = camera_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(camera, field, value)
    
    db.commit()
    db.refresh(camera)
    return camera


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(
    camera_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a camera"""
    camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    db.delete(camera)
    db.commit()
    return None