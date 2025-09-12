"""Pydantic models for ping/pong functionality"""
from pydantic import BaseModel


class PingRequest(BaseModel):
    data: str


class PongResponse(BaseModel):
    message: str
    status: str = "success"