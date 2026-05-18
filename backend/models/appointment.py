from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    """
    A Pydantic model for an appointment. Forces structure in appointment data.
    """
    name: str
    service: str