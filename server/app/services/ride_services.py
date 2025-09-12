"""Ride service with database operations"""
from sqlalchemy.orm import Session
from app.database.models import Ride, User
from app.models.ride import RideCreate, RideUpdate
from typing import List, Optional
from datetime import datetime


class RideService:
    @staticmethod
    def create_ride(db: Session, ride_data: RideCreate) -> Ride:
        """Create a new ride request"""
        db_ride = Ride(**ride_data.dict())
        db.add(db_ride)
        db.commit()
        db.refresh(db_ride)
        return db_ride
    
    @staticmethod
    def get_ride_by_id(db: Session, ride_id: int) -> Optional[Ride]:
        """Get ride by ID"""
        return db.query(Ride).filter(Ride.id == ride_id).first()
    
    @staticmethod
    def get_rides_by_passenger(db: Session, passenger_id: int) -> List[Ride]:
        """Get all rides for a passenger"""
        return db.query(Ride).filter(Ride.passenger_id == passenger_id).all()
    
    @staticmethod
    def get_rides_by_driver(db: Session, driver_id: int) -> List[Ride]:
        """Get all rides for a driver"""
        return db.query(Ride).filter(Ride.driver_id == driver_id).all()
    
    @staticmethod
    def get_available_rides(db: Session) -> List[Ride]:
        """Get rides that are available for drivers to accept"""
        return db.query(Ride).filter(Ride.status == "requested").all()
    
    @staticmethod
    def accept_ride(db: Session, ride_id: int, driver_id: int) -> Optional[Ride]:
        """Driver accepts a ride"""
        db_ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if db_ride and db_ride.status == "requested":
            db_ride.driver_id = driver_id
            db_ride.status = "accepted"
            db_ride.accepted_at = datetime.utcnow()
            db.commit()
            db.refresh(db_ride)
        return db_ride
    
    @staticmethod
    def start_ride(db: Session, ride_id: int) -> Optional[Ride]:
        """Start a ride"""
        db_ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if db_ride and db_ride.status == "accepted":
            db_ride.status = "in_progress"
            db_ride.started_at = datetime.utcnow()
            db.commit()
            db.refresh(db_ride)
        return db_ride
    
    @staticmethod
    def complete_ride(db: Session, ride_id: int, fare: float, distance_km: float, duration_minutes: int) -> Optional[Ride]:
        """Complete a ride"""
        db_ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if db_ride and db_ride.status == "in_progress":
            db_ride.status = "completed"
            db_ride.completed_at = datetime.utcnow()
            db_ride.fare = fare
            db_ride.distance_km = distance_km
            db_ride.duration_minutes = duration_minutes
            db.commit()
            db.refresh(db_ride)
        return db_ride