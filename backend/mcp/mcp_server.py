import os
import sys
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

# Add parent directory to path to allow importing from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Camera, Alert
    from config import settings
    
    # Force absolute path for SQLite to avoid issues when running from subdirectories
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if settings.USE_SQLITE:
        db_path = os.path.join(backend_dir, "vigilai.db")
        database_url = f"sqlite:///{db_path}"
    else:
        database_url = settings.DATABASE_URL
        
    # Create engine without echo to avoid polluting stdout
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if settings.USE_SQLITE else {},
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    HAS_DB = True
except ImportError:
    HAS_DB = False

# Initialize FastMCP server
mcp = FastMCP("VigilAI")

@mcp.tool()
def get_alerts(severity: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Retrieve recent security alerts from the database.
    
    Args:
        severity: Severity level (low, medium, high, critical)
        limit: Number of alerts to return (default 10)
    """
    if not HAS_DB:
        return {"error": "Database connection not available or models not found."}
        
    db = SessionLocal()
    try:
        from models import Alert
        query = db.query(Alert)
        if severity:
            query = query.filter(Alert.severity == severity)
        
        alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
        
        return {
            "result": [
                {
                    "id": str(alert.id),
                    "camera_id": str(alert.camera_id),
                    "severity": alert.severity,
                    "status": alert.status,
                    "description": alert.description,
                    "timestamp": alert.created_at.isoformat() if alert.created_at else None
                } for alert in alerts
            ]
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@mcp.tool()
def notify_authorities(alert_id: str, department: str = "Police Control Room") -> Dict[str, Any]:
    """Notify local authorities about a critical security alert.
    
    Args:
        alert_id: The UUID of the critical alert.
        department: The department to notify (default: Police Control Room).
    """
    # In a real system, this would call an external API or dispatch system
    print(f"MCP NOTIFICATION: Alert {alert_id} dispatched to {department}")
    return {
        "status": "success",
        "message": f"Alert {alert_id} successfully sent to {department}",
        "timestamp": "2026-01-20T18:15:00Z"
    }

if __name__ == "__main__":
    mcp.run()
