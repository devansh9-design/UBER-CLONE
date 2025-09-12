"""Ping/Pong API routes with database logging"""
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.ping import PingRequest, PongResponse
from app.services.ping_service import PingService
from app.database.connection import get_db

router = APIRouter(prefix="/api", tags=["ping"])


@router.post("/ping", response_model=PongResponse)
async def ping_endpoint(request: PingRequest, req: Request, db: Session = Depends(get_db)):
    """
    Ping endpoint that responds with pong when data is 'ping' and logs to database
    """
    try:
        client_ip = req.client.host
        service = PingService()
        response = service.process_ping(request, db, client_ip)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mini-uber-api"}