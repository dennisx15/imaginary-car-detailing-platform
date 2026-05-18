from fastapi import APIRouter
from backend.models.appointment import AppointmentCreate

from backend.database.connection import SessionLocal
from backend.database.models import Appointment

router = APIRouter()

@router.post("/appointments")
def create_appointment(appointment: AppointmentCreate):
    """
    Expect incoming JSON data and store it in appointment.
    """
    db = SessionLocal() # create a new database session, kinda like start a conversation with the database

    db_appointment = Appointment(
        name=appointment.name,
        service=appointment.service
    ) # creates a SQLAlchemy ORM object. This is like a Python representation of a row in the appointments table.

    db.add(db_appointment) # tells SQLAlchemy: “track this object for insertion.” notthing is actually sent to the database yet.
    db.commit() # this is when the SQL INSERT statement is actually sent to the database. The new appointment is now stored in the database.
    db.refresh(db_appointment) # reloads object from database. Because PostgreSQL automatically generates an id for new rows, this is how we get the generated id back into our db_appointment object.

    print(appointment)
    return {
        "message": "Appointment received",
        "data": db_appointment.id # return the id of the new appointment
    }