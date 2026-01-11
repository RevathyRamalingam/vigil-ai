"""
Machine Learning processor for video/image analysis using YOLOv8
"""
from ultralytics import YOLO
import cv2
import requests
from pathlib import Path
import tempfile
import numpy as np
from typing import List, Dict
import logging

from config import settings

logger = logging.getLogger(__name__)


class MLProcessor:
    """ML processor for detecting objects/activities in media"""
    
    def __init__(self):
        """Initialize YOLO model"""
        try:
            self.model = YOLO(settings.MODEL_PATH)
            logger.info(f"Loaded model from {settings.MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
        
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
        # Define detection type mapping
        self.detection_types = {
            # Weapons
            'knife': 'weapon',
            'gun': 'weapon',
            'rifle': 'weapon',
            
            # People/Crowd
            'person': 'person',
            
            # Vehicles
            'car': 'vehicle',
            'truck': 'vehicle',
            'bus': 'vehicle',
            'motorcycle': 'vehicle',
            
            # Other
            'fire': 'fire',
            'smoke': 'smoke'
        }
    
    def process_video(self, video_url: str) -> List[Dict]:
        """
        Process video file and detect objects/activities
        
        Args:
            video_url: URL or path to video file
            
        Returns:
            List of detection dictionaries
        """
        detections = []
        
        # Download video to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            video_path = tmp_file.name
            
            # Download from URL
            if video_url.startswith('http'):
                response = requests.get(video_url)
                tmp_file.write(response.content)
            else:
                # Copy local file
                with open(video_url, 'rb') as f:
                    tmp_file.write(f.read())
        
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = 0
            
            # Process frames at specified FPS
            frame_skip = max(1, fps // settings.FRAME_EXTRACTION_FPS)
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every Nth frame
                if frame_count % frame_skip == 0:
                    frame_detections = self._process_frame(frame, frame_count)
                    detections.extend(frame_detections)
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Processed {frame_count} frames, found {len(detections)} detections")
            
        finally:
            # Cleanup temp file
            Path(video_path).unlink(missing_ok=True)
        
        return detections
    
    def process_image(self, image_url: str) -> List[Dict]:
        """
        Process single image and detect objects
        
        Args:
            image_url: URL or path to image file
            
        Returns:
            List of detection dictionaries
        """
        # Download image
        if image_url.startswith('http'):
            response = requests.get(image_url)
            image_array = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        else:
            image = cv2.imread(image_url)
        
        return self._process_frame(image, frame_number=0)
    
    def _process_frame(self, frame: np.ndarray, frame_number: int) -> List[Dict]:
        """
        Process a single frame and return detections
        
        Args:
            frame: OpenCV image array
            frame_number: Frame number in video
            
        Returns:
            List of detection dictionaries
        """
        detections = []
        
        # Run inference
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)
        
        # Parse results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get detection info
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0])
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Map to our detection types
                detection_type = self.detection_types.get(class_name.lower(), 'unknown')
                
                # Skip if unknown or low confidence
                if detection_type == 'unknown' or confidence < self.confidence_threshold:
                    continue
                
                detection = {
                    'type': detection_type,
                    'original_class': class_name,
                    'confidence': confidence,
                    'frame_number': frame_number,
                    'bbox': {
                        'x': int(x1),
                        'y': int(y1),
                        'width': int(x2 - x1),
                        'height': int(y2 - y1)
                    }
                }
                
                detections.append(detection)
        
        return detections
    
    def is_crowd(self, detections: List[Dict]) -> bool:
        """
        Determine if there's a crowd based on person detections
        
        Args:
            detections: List of detections from a frame
            
        Returns:
            bool: True if crowd detected
        """
        person_count = sum(1 for d in detections if d['type'] == 'person')
        return person_count >= 20  # Threshold for crowd