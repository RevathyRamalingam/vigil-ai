"""
Alerts Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from database import get_db
from db import models
import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Alert])
def list_alerts(
    status_filter: Optional[str] = Query(None, description="Filter by status: new, acknowledged, resolved"),
    severity: Optional[str] = Query(None, description="Filter by severity: low, medium, high, critical"),
    camera_id: Optional[UUID] = Query(None, description="Filter by camera ID"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get list of alerts with optional filters
    """
    query = db.query(models.Alert)
    
    # Apply filters
    if status_filter:
        query = query.filter(models.Alert.status == status_filter)
    if severity:
        query = query.filter(models.Alert.severity == severity)
    if camera_id:
        query = query.filter(models.Alert.camera_id == camera_id)
    
    # Order by most recent first
    alerts = query.order_by(desc(models.Alert.created_at)).offset(skip).limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db)
):
    """Get alert details by ID"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.patch("/{alert_id}", response_model=schemas.Alert)
def update_alert_status(
    alert_id: UUID,
    alert_update: schemas.AlertUpdate,
    db: Session = Depends(get_db)
):
    """
    Update alert status (acknowledge or resolve)
    """
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    update_data = alert_update.dict(exclude_unset=True)
    
    # Handle status changes with timestamps
    if "status" in update_data:
        if update_data["status"] == "acknowledged" and not alert.acknowledged_at:
            alert.acknowledged_at = datetime.utcnow()
        elif update_data["status"] == "resolved" and not alert.resolved_at:
            alert.resolved_at = datetime.utcnow()
    
    # Update fields
    for field, value in update_data.items():
        setattr(alert, field, value)
    
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/stats/summary")
def get_alert_stats(
    db: Session = Depends(get_db)
):
    """Get alert statistics summary"""
    total_alerts = db.query(models.Alert).count()
    new_alerts = db.query(models.Alert).filter(models.Alert.status == "new").count()
    acknowledged = db.query(models.Alert).filter(models.Alert.status == "acknowledged").count()
    resolved = db.query(models.Alert).filter(models.Alert.status == "resolved").count()
    
    # Count by severity
    critical = db.query(models.Alert).filter(models.Alert.severity == "critical").count()
    high = db.query(models.Alert).filter(models.Alert.severity == "high").count()
    medium = db.query(models.Alert).filter(models.Alert.severity == "medium").count()
    low = db.query(models.Alert).filter(models.Alert.severity == "low").count()
    
    return {
        "total": total_alerts,
        "by_status": {
            "new": new_alerts,
            "acknowledged": acknowledged,
            "resolved": resolved
        },
        "by_severity": {
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low
        }
    }