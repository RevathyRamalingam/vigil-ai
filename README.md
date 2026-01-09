VigilAI – Smart Surveillance Incident Detection System 🛰️🛡️

VigilAI is a cloud-based ML system designed to:

Monitor: Ingest live feeds from street cameras and high-traffic city areas.
Analyze: Automatically detect suspicious activities using Machine Learning.
Act: Provide real-time alerts to Police control rooms via a centralized dashboard.

Complete Project Plan & Implementation Guide

1. Project Overview
Smart Surveillance Incident Detection System
A cloud-based system for automated incident detection from surveillance footage using ML. Allows security personnel to upload video/images, automatically detect suspicious activities, and manage alerts through a real-time dashboard.

Key Features:
Camera/location management
Video/image upload and processing
ML-based activity detection (weapons, crowds, accidents)
Real-time alert dashboard
Historical incident search and analytics

2. System Architecture
Architecture Diagram:
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/Vite)                    │
│  - Dashboard  - Camera Mgmt  - Alerts  - Analytics          │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API / WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐         │
│  │   API      │  │   Auth      │  │   WebSocket  │         │
│  │ Controller │  │  Service    │  │   Handler    │         │
│  └─────┬──────┘  └──────┬──────┘  └──────┬───────┘         │
│        │                │                 │                 │
│  ┌─────▼────────────────▼─────────────────▼───────┐         │
│  │           Business Logic Layer                 │         │
│  │  - Camera Service  - Processing Service        │         │
│  │  - Alert Service   - Analytics Service         │         │
│  └─────┬──────────────────────────────────┬───────┘         │
└────────┼──────────────────────────────────┼─────────────────┘
         │                                  │
    ┌────▼─────┐                      ┌─────▼──────┐
    │PostgreSQL│                      │   Redis    │
    │ Database │                      │Task Queue  │
    └──────────┘                      └─────┬──────┘
                                            │
                                      ┌─────▼──────┐
                                      │ML Worker(s)│
                                      │  - YOLOv8  │
                                      │  - Frame   │
                                      │  Extraction│
                                      └─────┬──────┘
                                            │
                                      ┌─────▼──────┐
                                      │   MinIO    │
                                      │ (S3-like)  │
                                      │  Storage   │
                                      └────────────┘

3. Technology Stack
Frontend
Framework: React 18 with Vite
UI Library: shadcn/ui + Tailwind CSS
State Management: React Query + Zustand
Real-time: WebSocket (socket.io-client)
Testing: Vitest + React Testing Library
API Client: Axios with OpenAPI types
Backend
Framework: FastAPI (Python 3.11+)
API Docs: OpenAPI 3.0 (auto-generated)
Database: PostgreSQL + SQLAlchemy ORM
Task Queue: Redis + Celery
Testing: pytest + pytest-asyncio
Auth: JWT tokens
ML & Processing
Model: YOLOv8 (Ultralytics)
Video Processing: OpenCV + FFmpeg
Detection Classes: Weapons, crowds, vehicles
Framework: PyTorch
Storage: MinIO (S3-compatible)
DevOps
Containerization: Docker + Docker Compose
CI/CD: GitHub Actions
Deployment: Railway / Render
Monitoring: Prometheus + Grafana (optional)
Environments: Dev (SQLite) / Prod (Postgres)

4. Database Schema
-- Cameras Table
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Media Uploads Table
CREATE TABLE media_uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id),
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'video' or 'image'
    file_url VARCHAR(1000) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'pending',
    processed_at TIMESTAMP
);

-- Detections Table
CREATE TABLE detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    media_id UUID REFERENCES media_uploads(id),
    frame_number INT,
    detection_type VARCHAR(100) NOT NULL, -- 'weapon', 'crowd', 'accident'
    confidence DECIMAL(5, 4) NOT NULL,
    bounding_box JSONB, -- {x, y, width, height}
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts Table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    detection_id UUID REFERENCES detections(id),
    camera_id UUID REFERENCES cameras(id),
    severity VARCHAR(50) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    status VARCHAR(50) DEFAULT 'new', -- 'new', 'acknowledged', 'resolved'
    description TEXT,
    thumbnail_url VARCHAR(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    acknowledged_by VARCHAR(255),
    notes TEXT
);

-- Analytics/Events Table
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    camera_id UUID REFERENCES cameras(id),
    metadata JSONB,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);
CREATE INDEX idx_media_status ON media_uploads(processing_status);
CREATE INDEX idx_detections_type ON detections(detection_type);

5. API Contract (OpenAPI)
Key endpoints to implement:

GET
/api/cameras
List all cameras
POST
/api/cameras
Register new camera
GET
/api/cameras/{id}
Get camera details
PUT
/api/cameras/{id}
Update camera
POST
/api/media/upload
Upload video/image
GET
/api/media/{id}
Get upload status
GET
/api/alerts
List alerts (paginated, filtered)
GET
/api/alerts/{id}
Get alert details
PATCH
/api/alerts/{id}
Update alert status
GET
/api/analytics/dashboard
Get dashboard stats
WS
/ws/alerts
Real-time alert notifications

6. Implementation Plan
Phase 1: Setup & Foundation (Week 1)
Initialize frontend (Vite + React) from Lovable
Setup backend FastAPI project structure
Configure Docker Compose (postgres, redis, minio)
Define OpenAPI specifications
Setup database migrations (Alembic)
Create CI/CD pipeline (GitHub Actions)
Phase 2: Core Backend (Week 2)
Implement camera management endpoints
Implement media upload endpoint with MinIO
Setup Celery workers for async processing
Implement video frame extraction
Integrate YOLOv8 for detection
Write backend unit tests (pytest)
Phase 3: Frontend Development (Week 2-3)
Build camera management UI
Build upload interface with progress
Build alerts dashboard with real-time updates
Build alert detail view with actions
Build analytics/statistics page
Write frontend tests (Vitest)
Phase 4: Integration & Testing (Week 3)
Implement WebSocket for real-time alerts
Write integration tests (API + DB)
End-to-end testing
Performance optimization
Security hardening (CORS, rate limiting)
Phase 5: Deployment & Documentation (Week 4)
Deploy to Railway/Render
Setup production database
Configure environment variables
Write comprehensive README
Document AI development process (AGENTS.md)
Create demo video/screenshots

7. ML Implementation Details
Detection Classes:
Weapons: guns, knives (high severity)
Crowd: unusual gatherings >20 people (medium severity)
Vehicles: abandoned vehicles, accidents (medium severity)
Fire/Smoke: fire detection (critical severity)
Person: person detection for counting (low severity)
Processing Pipeline:
1. Video Upload → MinIO Storage
2. Celery Task Created
3. Worker Extracts Frames (1 fps)
4. Each Frame → YOLOv8 Detection
5. Confidence > 0.6 → Create Detection Record
6. Group Detections → Create Alert
7. WebSocket Notification → Frontend
8. Thumbnail Generated → Stored in MinIO
Sample Code Snippet:
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')  # or custom trained model

def process_frame(frame, frame_num):
    results = model(frame, conf=0.6)
    detections = []
    
    for r in results:
        for box in r.boxes:
            detection = {
                'class': model.names[int(box.cls)],
                'confidence': float(box.conf),
                'bbox': box.xyxy.tolist(),
                'frame': frame_num
            }
            detections.append(detection)
    
    return detections

8. Testing Strategy

9. Deployment Guide

10. Documentation Requirements

11. Scoring Checklist
Next Steps
Set up GitHub repository with proper .gitignore
Initialize frontend from Lovable export
Create FastAPI backend structure
Set up Docker Compose for local development
Start implementing Phase 1 tasks
Document AI assistance in AGENTS.md as you go
