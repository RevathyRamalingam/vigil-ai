"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID


# Camera Schemas
class CameraBase(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str = "active"


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = None


class Camera(CameraBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Media Upload Schemas
class MediaUploadBase(BaseModel):
    camera_id: UUID
    file_name: str
    file_type: str


class MediaUploadCreate(MediaUploadBase):
    file_url: str


class MediaUpload(MediaUploadBase):
    id: UUID
    file_url: str
    upload_time: datetime
    processing_status: str
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Detection Schemas
class DetectionBase(BaseModel):
    detection_type: str
    confidence: float
    frame_number: Optional[int] = None
    bounding_box: Optional[Dict] = None


class Detection(DetectionBase):
    id: UUID
    media_id: UUID
    detected_at: datetime
    
    class Config:
        from_attributes = True


# Alert Schemas
class AlertBase(BaseModel):
    severity: str
    description: Optional[str] = None


class AlertCreate(AlertBase):
    detection_id: UUID
    camera_id: UUID
    thumbnail_url: Optional[str] = None


class AlertUpdate(BaseModel):
    status: Optional[str] = None
    acknowledged_by: Optional[str] = None
    notes: Optional[str] = None


class Alert(AlertBase):
    id: UUID
    detection_id: UUID
    camera_id: UUID
    status: str
    thumbnail_url: Optional[str] = None
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


# Analytics Schemas
class DashboardStats(BaseModel):
    total_cameras: int
    active_cameras: int
    total_alerts: int
    alerts_today: int
    alerts_by_severity: Dict[str, int]
    recent_alerts: List[Alert]


# Pagination
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int