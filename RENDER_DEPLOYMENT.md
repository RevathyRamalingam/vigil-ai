# Deploying VigilAI to Render

This guide explains how to deploy the VigilAI project to Render using the included `render.yaml` Blueprint.

## Prerequisites
- A [Render](https://render.com) account.
- Your project pushed to a GitHub or GitLab repository.

## Deployment Steps

1. **Log in to Render**: Go to [dashboard.render.com](https://dashboard.render.com).
2. **Create a New Blueprint**:
   - Click the **"New +"** button and select **"Blueprint"**.
   - Connect your GitHub/GitLab repository.
   - Select the `vigil-ai` repository.
3. **Configure the Blueprint**:
   - Give your group of services a name (e.g., `vigilai-prod`).
   - Render will automatically detect the `render.yaml` file.
   - Review the services to be created:
     - `vigilai-db`: Managed PostgreSQL
     - `vigilai-redis`: Managed Redis
     - `vigilai-minio`: MinIO storage service
     - `vigilai-backend`: FastAPI Backend
     - `vigilai-frontend`: React/Vite Frontend
4. **Deploy**:
   - Click **"Apply"**.
   - Render will start provisioning the database, redis, and building the Docker images for the backend, frontend, and MinIO.

## Important Notes

### Data Persistence
> [!WARNING]
> While `vigilai-db` and `vigilai-redis` are persistent managed services, the `vigilai-minio` service uses a standard Docker Web Service on the free tier, meaning **any data uploaded to MinIO will be lost when the service restarts**.
> For production, consider using a Render disk (requires a paid plan) or switching to AWS S3.

### Environment Variables
The Blueprint automatically links the backend to the database and redis. However, you can manually override environment variables in the Render dashboard if needed:
- `POSTGRES_HOST`: (Managed)
- `REDIS_HOST`: (Managed)
- `MINIO_ENDPOINT`: `vigilai-minio:9000` (Internal)
- `USE_SQLITE`: `False`

### Accessing the App
Once the deployment is complete, the frontend will be accessible at the `.onrender.com` URL provided by Render for the `vigilai-frontend` service.
