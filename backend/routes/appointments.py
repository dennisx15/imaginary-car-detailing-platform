from fastapi import APIRouter, Header
from backend.models.appointment import AppointmentCreate
from jose import jwt

from backend.database.connection import SessionLocal
from backend.database.models import Appointment
from backend.routes.auth import ALGORITHM, SECRET_KEY

router = APIRouter()

@router.post("/appointments")
def create_appointment(appointment: AppointmentCreate, authorization: str = Header(None)):
    """
    Expect incoming JSON data and store it in appointment.
    """
    if not authorization:
        return {
        "message":
            "Authorization header missing"
            }

    db = SessionLocal() # create a new database session, kinda like start a conversation with the database

    token = authorization.split(" ")[1] # the token is in the format "Bearer {token}", so we split by space and take the second part to get the actual token string.

    payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
    user_id = payload["user_id"] # this is the user_id that we encoded in the token when we created it during login. We can use this user_id to associate the appointment with the user who made it.

    db_appointment = Appointment(
        name=appointment.name,
        service=appointment.service,
        phone_number=appointment.phone_number,
        notes=appointment.notes,
        user_id=user_id
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

@router.get("/appointments/{user_id}")
def get_appointments_by_user(user_id: int):
    """
    Get all appointments for a specific user from the database and return them as a list. The user_id is passed in the URL, and FastAPI automatically converts it to an integer because we specified user_id: int.
    """
    db = SessionLocal()
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all() # this translates to "SELECT * FROM appointments WHERE user_id = {user_id}" in SQL. The result is a list of Appointment objects that match the user_id.
    db.close()
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

@router.get("/my-appointments")
def get_my_appointments(authorization: str = Header(None)):
    """
    Get all appointments for the currently logged in user. This endpoint expects an Authorization header with a JWT token, which it decodes to get the user_id, and then queries the database for appointments with that user_id.
    """
    if not authorization:
        return {
        "message":
            "Authorization header missing"
            }

    db = SessionLocal()

    token = authorization.split(" ")[1]

    payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
    user_id = payload["user_id"]

    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
    db.close()
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

@router.delete("/my-appointments/{appointment_id}")
def user_delete_appointment(appointment_id: int, authorization: str = Header(None)):
    """
    delete an appointment from the database by id, but only if it belongs to the currently logged in user. This endpoint expects an Authorization header with a JWT token, which it decodes to get the user_id, and then checks if the appointment with the given id has that user_id before deleting it.
    """

    if not authorization:
        return {
        "message":
            "Authorization header missing"
            }

    db = SessionLocal()

    token = authorization.split(" ")[1]

    payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
    user_id = payload["user_id"]

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == user_id).first() # this translates to "SELECT * FROM appointments WHERE id = {appointment_id} AND user_id = {user_id} LIMIT 1" in SQL. It returns the first appointment that matches the id and belongs to the user, or None if no appointment is found.

    if appointment:
        db.delete(appointment)
        db.commit()
        message = "Appointment deleted"
    else:
        message = "Appointment not found or does not belong to user"

    db.close()
    return {"message": message}