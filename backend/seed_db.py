import uuid
from datetime import datetime, timezone
import os
import sys

# Add the current directory to sys.path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from db import models

def seed():
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Add a Camera if it doesn't exist
        camera_name = "Main Entrance"
        db_camera = db.query(models.Camera).filter(models.Camera.name == camera_name).first()
        
        if not db_camera:
            camera_id = uuid.uuid4()
            db_camera = models.Camera(
                id=camera_id,
                name=camera_name,
                location="Ground Floor Lobby",
                status="active",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.add(db_camera)
            db.flush()
            print(f"Added camera: {camera_name}")
        else:
            camera_id = db_camera.id
            print(f"Camera '{camera_name}' already exists.")

        # 2. Add a Media Upload if it doesn't exist
        file_name = "security_footage_001.mp4"
        db_media = db.query(models.MediaUpload).filter(models.MediaUpload.file_name == file_name).first()
        
        if not db_media:
            media_id = uuid.uuid4()
            db_media = models.MediaUpload(
                id=media_id,
                camera_id=camera_id,
                file_name=file_name,
                file_type="video",
                file_url="http://localhost:9000/vigilai-uploads/security_footage_001.mp4",
                upload_time=datetime.now(timezone.utc),
                processing_status="completed"
            )
            db.add(db_media)
            db.flush()
            print(f"Added media: {file_name}")
            
            # 3. Add a Detection
            detection_id = uuid.uuid4()
            db_detection = models.Detection(
                id=detection_id,
                media_id=media_id,
                frame_number=120,
                detection_type="weapon",
                confidence=0.95,
                detected_at=datetime.now(timezone.utc)
            )
            db.add(db_detection)
            db.flush()
            
            # 4. Add an Alert
            alert_id = uuid.uuid4()
            db_alert = models.Alert(
                id=alert_id,
                detection_id=detection_id,
                camera_id=camera_id,
                severity="critical",
                status="new",
                description="Potential weapon detected at Main Entrance",
                created_at=datetime.now(timezone.utc)
            )
            db.add(db_alert)
            print("Added sample detection and alert for the new media.")
        else:
            print(f"Media '{file_name}' already exists. Skipping entry to avoid duplicates.")
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
