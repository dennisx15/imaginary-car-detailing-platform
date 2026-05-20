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
        service=appointment.service,
        phone_number=appointment.phone_number,
        notes=appointment.notes
    ) # creates a SQLAlchemy ORM object. This is like a Python representation of a row in the appointments table.

    db.add(db_appointment) # tells SQLAlchemy: “track this object for insertion.” notthing is actually sent to the database yet.
    db.commit() # this is when the SQL INSERT statement is actually sent to the database. The new appointment is now stored in the database.
    db.refresh(db_appointment) # reloads object from database. Because PostgreSQL automatically generates an id for new rows, this is how we get the generated id back into our db_appointment object.

    print(appointment)
    return {
        "message": "Appointment received",
        "data": db_appointment.id # return the id of the new appointment
    }

@router.get("/appointments")
def get_appointments():
    """
    Get all appointments from the database and return them as a list.
    """
    db = SessionLocal()
    appointments = db.query(Appointment).all() # this is how you query the database with SQLAlchemy. It translates to "SELECT * FROM appointments" in SQL. The result is a list of Appointment objects.
    db.close() # close the database session to free up resources. It's important to do this after you're done with the database.
    return [
        {
            "id": appointment.id,
            "name": appointment.name,
            "phone_number": appointment.phone_number,
            "service": appointment.service,
            "notes": appointment.notes
        }

        for appointment in appointments
    ]

@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    """
    delete an appointment from the database by id. The appointment_id is passed in the URL, and FastAPI automatically converts it to an integer because we specified appointment_id: int.
    """

    db = SessionLocal()
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first() # this translates to "SELECT * FROM appointments WHERE id = {appointment_id} LIMIT 1" in SQL. It returns the first appointment that matches the id, or None if no appointment is found.
    if appointment:
        db.delete(appointment)
        db.commit()
    db.close()
    return {"message": "Appointment deleted"}