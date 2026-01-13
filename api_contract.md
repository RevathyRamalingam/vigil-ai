# API Contract (OpenAPI)

VigilAI uses FastAPI, which automatically generates an OpenAPI 3.0 specification. This specification serves as the formal contract between the backend and frontend.

## Key Endpoints

### Surveillance Scanning
- **POST `/api/scan`**: Triggers an ML-based scan of the videos in the static directory.
  - **Response**: `{"alert": bool, "total_scanned": int, "results": dict}`

### Camera Management
- **GET `/api/cameras`**: List all registered cameras.
- **POST `/api/cameras`**: Register a new surveillance camera.
- **GET `/api/cameras/{id}`**: Get detailed info for a specific camera.

### Media & Alerts
- **POST `/api/media/upload`**: Upload video or image for processing.
- **GET `/api/alerts`**: Fetch a list of all detected incidents/alerts.
- **PATCH `/api/alerts/{id}`**: Update an alert status (e.g., Acknowledged, Resolved).

### Real-time Notifications
- **WS `/ws/alerts`**: WebSocket endpoint for real-time alert broadcasts.

## Specification Access
The full, interactive contract can be accessed during development at:
- Swagger UI: `http://localhost:8000/docs`
- JSON Specification: `http://localhost:8000/openapi.json`
