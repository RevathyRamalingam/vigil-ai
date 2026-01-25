VigilAI – Smart Surveillance Incident Detection System 🛰️🛡️

VigilAI is a cloud-based Machine Learning system designed to enhance public safety by monitoring live surveillance feeds and automatically detecting suspicious activities.

## 1. Problem Description
In high-traffic city areas, monitoring hundreds of camera feeds manually is inefficient and prone to human error. Security personnel often miss critical incidents due to fatigue or cognitive overload.

While crime rates are increasing year after year, cases of rape, kidnapping and other violent assault are also on the rise. Monitoring entire city using manual task force may seem highly inefficient and time-consuming. It's high time to use AI to prevent such incidents.

**VigilAI addresses this by providing:**
- **Automated Monitoring**: Ingests live streams or static video footage. Currently, it is only supported for static video footage. Support for live streams is in progress.
- **Incident Detection**: Uses YOLOv8 ML model to identify weapons, fire, smoke, and unusual crowd densities.
- **Real-time Alerting**: Instantly notifies police control rooms via a WebSocket-powered dashboard by AI Agent(McpClient)

## 2. AI system development (tools, workflow, MCP)

### 2.1 AI System Development

AGENTS.md file contains the details of the AI system development, the prompts used to create front-end, backend and database, and the tools used to create the system.

The React FE shows a surveillance dashboard where the area is monitored, when the scan button is pressed the video is scanned for any suspicious activity in the neighbourhood and reports to the cop control room. For demo purpose, the video is static and the scan button toggles between normal and suspicious video to show the results.

The workflow starts from the FE UI, as user clicks on the scan button, the video is sent to the backend via API call. The processed result is sent to the MCP via API call. The MCP then sends the results to the FE UI via API call. Celery task queue is used to process the video in the background. The videos are stored in MinIO and tables containing metadata about the video is stored in PostgreSQL. Redis Server is the inmemory DB used to cache the results.

### 2.2 System Architecture & Technologies

### Architecture Overview
The system follows a modern decoupled architecture:
- **Frontend**: A responsive React dashboard that displays live status and recent alerts. Currently, it is only supported for static video footage. Support for live streams is in progress.
- **Backend**: A FastAPI-based REST API that handles logic, database persistence, and ML orchestration.
- **ML Processor**: A dedicated layer using YOLOv8 for frame-by-frame analysis.
- **Persistence**: PostgreSQL for structured data and MinIO (S3-compatible) for video/image storage.
- **Real-time**: WebSockets and McpClient using ToyAIKit for push-based notifications to the dashboard.
- CI/CD pipeline for running automated testcases covering Front-end(FE) and Backend(BE) using GitHubWorkflow for every code push/PR.
Two testcases for FE covering dashboard and scan button functionality is covered in the FE testcases. BE testcases for checking video upload and scan button functionality is added.

### Technology Role
- **FastAPI (Backend)**: Chosen for its high performance and native async support, serving as the API contract (OpenAPI) provider.
- **React 18 & Vite (Frontend)**: Provides a fast, interactive UI using Shadcn/ui for premium aesthetics.
- **YOLOv8 (ML)**: The state-of-the-art model for balanced speed and accuracy in object detection.
- **PostgreSQL**: Ensures reliable storage of camera metadata, detection history, and alert logs.
- **Docker**: Containerizes the entire stack for seamless reproducibility across environments.
- **Cloud**: Render is used for hosting the application and the render.yaml file is used for deployment.
- **CI/CD**: GitHub Actions is used for running automated testcases covering Front-end(FE) and Backend(BE) using GitHubWorkflow for every code push/PR.

## 3. AI System Development
This project was developed with significant AI assistance, documented in detail in [AGENTS.md](AGENTS.md). The development process utilized agentic loops for planning, implementation, and automated verification.

## 4. Getting Started (Reproducibility)

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js & NPM (for local development)

### Quick Start (Docker)

> git clone <projectrepo>
> pip install -r requirements.txt

The entire system can be run with a single command:
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8080`.
For demo purpose toggle option with normal and suspicious video is included. When scan now button is pressed, the video is analyzed and alerts are sent to the MCP. The agent notifies the dashboard.

Demo Video: https://www.loom.com/share/ae5c25a3532a4ab1a7fb793efabe7c55

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
### Integration tests (Playwright)
```bash
npm init playwright@latest (to install playwright)
docker-compose up --build (to start the containers)
npx playwright test --ui (to run the tests)
```
The integration tests are integrated in the CI/CD pipeline in GitHub Actions.

## 7. Database Integration
VigilAI supports both SQLite (Development) and PostgreSQL (Production).
- **SQLite**: Automatic configuration when running locally for easy setup.
- **Postgres**: Used in the Docker environment for high availability and persistence.

## 8. CI/CD
We use GitHub Actions to automatically run tests and lint checks on every push to `main`.
- **CI Pipeline**: [.github/workflows/tests.yml](.github/workflows/ci-cd.yml)
- The pipeline automatically deploys the application whenever code change is pushed to `main`. https://github.com/RevathyRamalingam/vigil-ai/actions/runs/21319887609

