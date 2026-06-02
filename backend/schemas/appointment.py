from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from backend.schemas.service import ServiceResponse # Assuming a schema for services


class AppointmentCreate(BaseModel):
    """
    A Pydantic model for an appointment. Forces structure in appointment data.
    """
    name: str
    phone_number: str
    service_id: int
    notes: str
    date: datetime


class AppointmentResponse(BaseModel):
    name: str
    id: int
    user_id: int
    phone_number: str
    date: datetime
    notes: Optional[str]
    service_id: int
    
    # 🔄 Nested object containing the full definition (name, price, description)
    service: ServiceResponse 

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy ORM objects smoothly