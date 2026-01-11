"""
MinIO Storage Service for file uploads
"""
from minio import Minio
from minio.error import S3Error
from fastapi import UploadFile
import io
import uuid
from datetime import timedelta

from config import settings


class StorageService:
    """Service for handling file storage using MinIO (S3-compatible)"""
    
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            print(f"Error checking/creating bucket: {e}")
    
    async def upload_file(self, file: UploadFile) -> str:
        """
        Upload file to MinIO storage
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            str: URL of uploaded file
        """
        # Generate unique filename
        file_ext = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        
        # Read file content
        content = await file.read()
        content_size = len(content)
        
        # Upload to MinIO
        try:
            self.client.put_object(
                self.bucket_name,
                unique_filename,
                io.BytesIO(content),
                content_size,
                content_type=file.content_type
            )
            
            # Generate accessible URL
            file_url = f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{unique_filename}"
            return file_url
            
        except S3Error as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def get_file_url(self, filename: str, expires: timedelta = timedelta(hours=1)) -> str:
        """
        Generate presigned URL for file access
        
        Args:
            filename: Name of file in storage
            expires: URL expiration time
            
        Returns:
            str: Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                filename,
                expires=expires
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to generate URL: {str(e)}")
    
    def delete_file(self, filename: str):
        """Delete file from storage"""
        try:
            self.client.remove_object(self.bucket_name, filename)
        except S3Error as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    def download_file(self, filename: str) -> bytes:
        """Download file from storage"""
        try:
            response = self.client.get_object(self.bucket_name, filename)
            return response.read()
        except S3Error as e:
            raise Exception(f"Failed to download file: {str(e)}")