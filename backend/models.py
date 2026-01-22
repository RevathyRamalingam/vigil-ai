"""
SQLAlchemy Database Models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from database import Base


class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String(50), default="active")
    stream_url = Column(String(1000), nullable=True)
    is_live = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    media_uploads = relationship("MediaUpload", back_populates="camera")
    alerts = relationship("Alert", back_populates="camera")


class MediaUpload(Base):
    __tablename__ = "media_uploads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"))
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # 'video' or 'image'
    file_url = Column(String(1000), nullable=False)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    camera = relationship("Camera", back_populates="media_uploads")
    detections = relationship("Detection", back_populates="media")


class Detection(Base):
    __tablename__ = "detections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_id = Column(UUID(as_uuid=True), ForeignKey("media_uploads.id"))
    frame_number = Column(Integer, nullable=True)
    detection_type = Column(String(100), nullable=False)  # 'weapon', 'crowd', 'accident', etc.
    confidence = Column(Float, nullable=False)
    bounding_box = Column(JSON, nullable=True)  # {x, y, width, height}
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    media = relationship("MediaUpload", back_populates="detections")
    alerts = relationship("Alert", back_populates="detection")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    detection_id = Column(UUID(as_uuid=True), ForeignKey("detections.id"))
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"))
    severity = Column(String(50), nullable=False)  # 'low', 'medium', 'high', 'critical'
    status = Column(String(50), default="new")  # 'new', 'acknowledged', 'resolved'
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    detection = relationship("Detection", back_populates="alerts")
    camera = relationship("Camera", back_populates="alerts")


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(100), nullable=False)
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"), nullable=True)
    meta = Column(JSON, nullable=True)
    occurred_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))