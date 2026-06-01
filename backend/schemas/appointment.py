from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    """
    A Pydantic model for an appointment. Forces structure in appointment data.
    """
    name: str
    phone_number: str
    service: str
    notes: str
    date: datetime