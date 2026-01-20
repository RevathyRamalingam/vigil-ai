"""
Celery configuration and tasks for async processing
"""
from celery import Celery
from config import settings
from ml_processor import MLProcessor
from database import SessionLocal
from db import models
from datetime import datetime, timezone
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "vigilai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Initialize ML processor
ml_processor = MLProcessor()


@celery_app.task(name="process_media")
def process_media_task(media_id: str):
    """
    Async task to process uploaded media (video/image)
    
    Steps:
    1. Update status to 'processing'
    2. Download file from storage
    3. Extract frames (for video) or process image
    4. Run ML detection on each frame
    5. Create detection records
    6. Create alerts for significant detections
    7. Update status to 'completed'
    """
    db = SessionLocal()
    
    try:
        # Get media record
        media = db.query(models.MediaUpload).filter(
            models.MediaUpload.id == UUID(media_id)
        ).first()
        
        if not media:
            logger.error(f"Media {media_id} not found")
            return
        
        logger.info(f"Processing media: {media_id}")
        
        # Update status
        media.processing_status = "processing"
        db.commit()
        
        # Process based on file type
        if media.file_type == "video":
            detections = ml_processor.process_video(media.file_url)
        else:  # image
            detections = ml_processor.process_image(media.file_url)
        
        # Save detections to database
        alert_created = False
        for detection_data in detections:
            detection = models.Detection(
                media_id=UUID(media_id),
                frame_number=detection_data.get('frame_number'),
                detection_type=detection_data['type'],
                confidence=detection_data['confidence'],
                bounding_box=detection_data.get('bbox')
            )
            db.add(detection)
            db.flush()
            
            # Create alert for high-confidence detections
            if detection_data['confidence'] >= 0.7:
                severity = _determine_severity(detection_data['type'], detection_data['confidence'])
                
                alert = models.Alert(
                    detection_id=detection.id,
                    camera_id=media.camera_id,
                    severity=severity,
                    description=f"{detection_data['type']} detected with {detection_data['confidence']:.2%} confidence",
                    thumbnail_url=detection_data.get('thumbnail_url')
                )
                db.add(alert)
                alert_created = True
        
        # Update media status
        media.processing_status = "completed"
        media.processed_at = datetime.now(timezone.utc)
        db.commit()
        
        logger.info(f"Media {media_id} processed successfully. Detections: {len(detections)}")
        
        # Broadcast alert if created (would integrate with WebSocket)
        if alert_created:
            logger.info(f"Alerts created for media {media_id}")
        
    except Exception as e:
        logger.error(f"Error processing media {media_id}: {str(e)}")
        media.processing_status = "failed"
        db.commit()
        raise
    
    finally:
        db.close()


def _determine_severity(detection_type: str, confidence: float) -> str:
    """Determine alert severity based on detection type and confidence"""
    
    # Critical detections
    if detection_type in ['weapon', 'gun', 'knife', 'fire']:
        return 'critical'
    
    # High severity
    if detection_type in ['accident', 'fight', 'violence']:
        return 'high'
    
    # Medium severity
    if detection_type in ['crowd', 'abandoned_vehicle', 'suspicious_activity']:
        return 'medium'
    
    # Low severity (default)
    return 'low'


@celery_app.task(name="cleanup_old_media")
def cleanup_old_media_task():
    """
    Periodic task to clean up old processed media
    Run this as a scheduled task (e.g., daily)
    """
    db = SessionLocal()
    try:
        # Implementation for cleaning up old files
        # Delete media older than 30 days, etc.
        pass
    finally:
        db.close()