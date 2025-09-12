"""Pydantic models for ride operations"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RideBase(BaseModel):
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    destination_address: str
    destination_latitude: float
    destination_longitude: float


class RideCreate(RideBase):
    passenger_id: int


class RideUpdate(BaseModel):
    driver_id: Optional[int] = None
    status: Optional[str] = None
    fare: Optional[float] = None
    distance_km: Optional[float] = None
    duration_minutes: Optional[int] = None


class RideResponse(RideBase):
    id: int
    passenger_id: int
    driver_id: Optional[int] = None
    status: str
    fare: Optional[float] = None
    distance_km: Optional[float] = None
    duration_minutes: Optional[int] = None
    created_at: datetime
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True