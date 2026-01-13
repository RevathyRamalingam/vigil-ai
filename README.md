VigilAI – Smart Surveillance Incident Detection System 🛰️🛡️

VigilAI is a cloud-based Machine Learning system designed to enhance public safety by monitoring live surveillance feeds and automatically detecting suspicious activities.

## 1. Problem Description
In high-traffic city areas, monitoring hundreds of camera feeds manually is inefficient and prone to human error. Security personnel often miss critical incidents due to fatigue or cognitive overload.

**VigilAI addresses this by providing:**
- **Automated Monitoring**: Ingests live streams or static video footage.
- **Incident Detection**: Uses YOLOv8 to identify weapons, fire, smoke, and unusual crowd densities.
- **Real-time Alerting**: Instantly notifies control rooms via a WebSocket-powered dashboard, allowing for rapid response.

## 2. System Architecture & Technologies

### Architecture Overview
The system follows a modern decoupled architecture:
- **Frontend**: A responsive React dashboard that displays live status and recent alerts.
- **Backend**: A FastAPI-based REST API that handles logic, database persistence, and ML orchestration.
- **ML Processor**: A dedicated layer using YOLOv8 for frame-by-frame analysis.
- **Persistence**: PostgreSQL for structured data and MinIO (S3-compatible) for video/image storage.
- **Real-time**: WebSockets for push-based notifications to the dashboard.

### Technology Roles
- **FastAPI (Backend)**: Chosen for its high performance and native async support, serving as the API contract (OpenAPI) provider.
- **React 18 & Vite (Frontend)**: Provides a fast, interactive UI using Shadcn/ui for premium aesthetics.
- **YOLOv8 (ML)**: The state-of-the-art model for balanced speed and accuracy in object detection.
- **PostgreSQL**: Ensures reliable storage of camera metadata, detection history, and alert logs.
- **Docker**: Containerizes the entire stack for seamless reproducibility across environments.

## 3. AI System Development
This project was developed with significant AI assistance, documented in detail in [AGENTS.md](AGENTS.md). The development process utilized agentic loops for planning, implementation, and automated verification.

## 4. Getting Started (Reproducibility)

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js & NPM (for local development)

### Quick Start (Docker)
The entire system can be run with a single command:
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8080`.

### Local Development Setup
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
2. **Frontend**:
   ```bash
   npm install
   npm run dev
   ```

## 5. API Contract
The API is strictly defined using OpenAPI 3.0. You can view the full specification and interact with the endpoints at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 6. Testing
### Backend Tests (Pytest)
```bash
cd backend
pytest
```
### Frontend Tests (Vitest)
```bash
npm run test
```

## 7. Database Integration
VigilAI supports both SQLite (Development) and PostgreSQL (Production).
- **SQLite**: Automatic configuration when running locally for easy setup.
- **Postgres**: Used in the Docker environment for high availability and persistence.

## 8. CI/CD
We use GitHub Actions to automatically run tests and lint checks on every push to `main`.
- **CI Pipeline**: [.github/workflows/tests.yml](.github/workflows/tests.yml)
