# 1. Use the Ultralytics base - it already has Torch and OpenCV pre-installed
FROM ultralytics/ultralytics:latest-python

# 2. Install only the extra system deps you need (ffmpeg is usually pre-installed here)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# 4. Remove --no-cache-dir to allow the buildkit cache to actually work
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# 5. Copy your backend code
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]