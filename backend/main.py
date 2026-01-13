"""
VigilAI FastAPI Backend - Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

from datetime import datetime
import models
import cameras, media, alerts, analytics, websocket
from config import settings
from database import engine, Base
from ultralytics import YOLO
import os
from sqlalchemy.orm import Session
from database import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Path to where your videos are stored in the project
VIDEO_DIR = "./static/videos"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting VigilAI Backend...")
    
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}. Running without DB persistence.")
    
    yield
    
    # Shutdown
    logger.info("Shutting down VigilAI Backend...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart Surveillance Incident Detection System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO('yolov8n.pt')

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception:
        yield None
    finally:
        if 'db' in locals() and db:
            db.close()

def analyze_single_video(video_path):
    """Processes one video using YOLO and returns a confidence score."""
    # This runs the YOLO model on the video path provided
    try:
        results = model(video_path, stream=True)
        
        highest_conf = 0.0
        
        for r in results:
            # If the AI detects anything (boxes), get the confidence
            if len(r.boxes) > 0:
                current_max = float(r.boxes.conf.max())
                if current_max > highest_conf:
                    highest_conf = current_max
            
            # Stop after first few frames to keep the 'Scan' button fast
            break 

        return highest_conf
    except Exception as e:
        logger.error(f"Error analyzing video {video_path}: {e}")
        return 0.0

@app.post("/api/scan")
async def scan_multiple_videos(db: Session = Depends(get_db)):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    VIDEO_DIR = os.path.join(BASE_DIR, "static", "videos")
    if not os.path.exists(VIDEO_DIR):

        os.makedirs(VIDEO_DIR)
        
    video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.avi'))]
    
    # Dictionary to store all results
    scan_report = {}
    alert_triggered = False

    for video_name in video_files:
        video_path = os.path.join(VIDEO_DIR, video_name)
        
        # 1. Run ML logic for this specific video
        confidence = analyze_single_video(video_path)
        is_alert = confidence > 0.5 # Example threshold
        
        if is_alert:
            alert_triggered = True

        # 2. Add to our return dictionary
        scan_report[video_name] = {
            "status": "Suspicious" if is_alert else "Normal",
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

    return {
        "alert": alert_triggered,
        "total_scanned": len(video_files),
        "results": scan_report
    }


# Include routers
try:
    import cameras, media, alerts, analytics, websocket
    app.include_router(cameras.router, prefix="/api/cameras", tags=["Cameras"])
    app.include_router(media.router, prefix="/api/media", tags=["Media"])
    app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
    app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
except Exception as e:
    logger.warning(f"Some routers could not be included due to dependency issues: {e}")





@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VigilAI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vigilai-backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )