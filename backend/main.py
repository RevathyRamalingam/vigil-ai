"""
VigilAI FastAPI Backend - Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

import cameras, media, alerts, analytics, websocket
from config import settings
from database import engine, Base
import tensorflow as tf
import os

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
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
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
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def analyze_single_video(video_path):
    """Processes one video and returns a confidence score."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if frame_count == 0:
        return 0.0
        
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return 0.0
    
    # ML Inference (using MobileNetV2 placeholder)
    img = cv2.resize(frame, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    
    predictions = model.predict(img)
    return float(np.max(predictions))

@app.post("/api/scan")
async def scan_multiple_videos(db: Session = Depends(get_db)):
    VIDEO_DIR = "./static/videos"
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

        # 2. Save entry to PostgreSQL for this specific video
        new_detection = models.Detection(
            video_name=video_name,
            alert_status=is_alert,
            confidence=round(confidence, 4),
            timestamp=datetime.now()
        )
        db.add(new_detection)
        
        # 3. Add to our return dictionary
        scan_report[video_name] = {
            "status": "Suspicious" if is_alert else "Normal",
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

    # Commit all detections at once
    db.commit()

    return {
        "overall_alert": alert_triggered,
        "total_scanned": len(video_files),
        "results": scan_report
    }


# Include routers
app.include_router(cameras.router, prefix="/api/cameras", tags=["Cameras"])
app.include_router(media.router, prefix="/api/media", tags=["Media"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


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