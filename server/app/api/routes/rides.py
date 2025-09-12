"""Ride management API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.ride import RideCreate, RideResponse, RideUpdate
from app.services.ride_services import RideService

router = APIRouter(prefix="/api/rides", tags=["rides"])


@router.post("/", response_model=RideResponse)
async def create_ride(ride_data: RideCreate, db: Session = Depends(get_db)):
    """Create a new ride request"""
    return RideService.create_ride(db, ride_data)


@router.get("/", response_model=List[RideResponse])
async def get_available_rides(db: Session = Depends(get_db)):
    """Get available rides for drivers"""
    return RideService.get_available_rides(db)


@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(ride_id: int, db: Session = Depends(get_db)):
    """Get ride by ID"""
    ride = RideService.get_ride_by_id(db, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride


@router.get("/passenger/{passenger_id}", response_model=List[RideResponse])
async def get_passenger_rides(passenger_id: int, db: Session = Depends(get_db)):
    """Get all rides for a passenger"""
    return RideService.get_rides_by_passenger(db, passenger_id)


@router.get("/driver/{driver_id}", response_model=List[RideResponse])
async def get_driver_rides(driver_id: int, db: Session = Depends(get_db)):
    """Get all rides for a driver"""
    return RideService.get_rides_by_driver(db, driver_id)


@router.put("/{ride_id}/accept", response_model=RideResponse)
async def accept_ride(ride_id: int, driver_id: int, db: Session = Depends(get_db)):
    """Driver accepts a ride"""
    ride = RideService.accept_ride(db, ride_id, driver_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found or cannot be accepted")
    return ride


@router.put("/{ride_id}/start", response_model=RideResponse)
async def start_ride(ride_id: int, db: Session = Depends(get_db)):
    """Start a ride"""
    ride = RideService.start_ride(db, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found or cannot be started")
    return ride


@router.put("/{ride_id}/complete", response_model=RideResponse)
async def complete_ride(
    ride_id: int, 
    fare: float, 
    distance_km: float, 
    duration_minutes: int, 
    db: Session = Depends(get_db)
):
    """Complete a ride"""
    ride = RideService.complete_ride(db, ride_id, fare, distance_km, duration_minutes)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found or cannot be completed")
    return ride