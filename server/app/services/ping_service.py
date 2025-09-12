"""Business logic for ping/pong functionality with database logging"""
from sqlalchemy.orm import Session
from app.models.ping import PingRequest, PongResponse
from app.database.models import PingLog


class PingService:
    @staticmethod
    def process_ping(ping_data: PingRequest, db: Session, ip_address: str = None) -> PongResponse:
        """Process ping request and return pong response with database logging"""
        
        if ping_data.data.lower() == "ping":
            response = PongResponse(message="pong")
        else:
            response = PongResponse(
                message=f"Received: {ping_data.data}, but expected 'ping'",
                status="warning"
            )
        
        # Log to database
        ping_log = PingLog(
            ping_data=ping_data.data,
            response_message=response.message,
            ip_address=ip_address
        )
        db.add(ping_log)
        db.commit()
        
        return response