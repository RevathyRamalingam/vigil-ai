"""
Analytics and Dashboard API Endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from db import models
import schemas

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard statistics
    """
    # Camera stats
    total_cameras = db.query(models.Camera).count()
    active_cameras = db.query(models.Camera).filter(models.Camera.status == "active").count()
    
    # Alert stats
    total_alerts = db.query(models.Alert).count()
    
    # Alerts today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    alerts_today = db.query(models.Alert).filter(
        models.Alert.created_at >= today_start
    ).count()
    
    # Alerts by severity
    alerts_by_severity = {
        "critical": db.query(models.Alert).filter(models.Alert.severity == "critical").count(),
        "high": db.query(models.Alert).filter(models.Alert.severity == "high").count(),
        "medium": db.query(models.Alert).filter(models.Alert.severity == "medium").count(),
        "low": db.query(models.Alert).filter(models.Alert.severity == "low").count()
    }
    
    # Recent alerts (last 10)
    recent_alerts = db.query(models.Alert).order_by(
        desc(models.Alert.created_at)
    ).limit(10).all()
    
    return {
        "total_cameras": total_cameras,
        "active_cameras": active_cameras,
        "total_alerts": total_alerts,
        "alerts_today": alerts_today,
        "alerts_by_severity": alerts_by_severity,
        "recent_alerts": recent_alerts
    }


@router.get("/timeline")
def get_alerts_timeline(
    days: int = Query(7, description="Number of days to include"),
    db: Session = Depends(get_db)
):
    """
    Get alerts timeline for the specified number of days
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Query alerts grouped by date
    timeline = db.query(
        func.date(models.Alert.created_at).label('date'),
        func.count(models.Alert.id).label('count'),
        models.Alert.severity
    ).filter(
        models.Alert.created_at >= start_date
    ).group_by(
        func.date(models.Alert.created_at),
        models.Alert.severity
    ).all()
    
    # Format results
    result = {}
    for entry in timeline:
        date_str = entry.date.isoformat()
        if date_str not in result:
            result[date_str] = {
                "date": date_str,
                "total": 0,
                "by_severity": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            }
        result[date_str]["by_severity"][entry.severity] = entry.count
        result[date_str]["total"] += entry.count
    
    return list(result.values())


@router.get("/detections/types")
def get_detection_types_stats(
    days: Optional[int] = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get statistics on detection types
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    detection_stats = db.query(
        models.Detection.detection_type,
        func.count(models.Detection.id).label('count'),
        func.avg(models.Detection.confidence).label('avg_confidence')
    ).filter(
        models.Detection.detected_at >= start_date
    ).group_by(
        models.Detection.detection_type
    ).all()
    
    return [
        {
            "type": stat.detection_type,
            "count": stat.count,
            "avg_confidence": round(float(stat.avg_confidence), 2)
        }
        for stat in detection_stats
    ]


@router.get("/cameras/activity")
def get_camera_activity(
    db: Session = Depends(get_db)
):
    """
    Get activity statistics per camera
    """
    camera_activity = db.query(
        models.Camera.id,
        models.Camera.name,
        models.Camera.location,
        func.count(models.Alert.id).label('alert_count')
    ).outerjoin(
        models.Alert
    ).group_by(
        models.Camera.id,
        models.Camera.name,
        models.Camera.location
    ).all()
    
    return [
        {
            "camera_id": str(activity.id),
            "camera_name": activity.name,
            "location": activity.location,
            "alert_count": activity.alert_count
        }
        for activity in camera_activity
    ]