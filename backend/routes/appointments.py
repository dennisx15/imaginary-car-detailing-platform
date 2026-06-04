from tokenize import String

from fastapi import APIRouter, Depends, Header, HTTPException
from backend.schemas.appointment import AppointmentCreate, AppointmentResponse

from backend.database.connection import SessionLocal
from backend.database.models import Appointment, Service

from backend.config import constants
from datetime import datetime

from backend.utils.security import *
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/appointments")
def create_appointment(appointment: AppointmentCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """
    Expect incoming JSON data and store it in appointment.
    :param appointment:
    :param user_id: fastAPI runs the get_current_user_id function before executing this route, and passes the returned user_id as an argument to this function. If the token is missing, invalid, or expired, get_current_user_id will raise an HTTPException with a 401 status code, which will automatically return a 401 response to the client and prevent this route from running.
    :param Session: fastAPI runs the get_db function before executing this route, and uses the yielded database session as the db argument for this function. After the route is done, get_db will automatically close the database session.
    """

    #Check if the requested service actually exists on the menu
    db_service = db.query(Service).get(appointment.service_id)
    if not db_service:
        raise HTTPException(
            status_code=404, 
            detail=f"Service with ID {appointment.service_id} does not exist"
        )
   

    existing = check_existing_appointment(db, appointment.date)
    if existing:
        print("Time slot already booked")
        raise HTTPException(
            status_code=400,
            detail="An appointment has already been made in this time slot") # this checks if there's already an appointment in the database with the same date and time as the one we're trying to create. If there is, it rolls back the transaction (undoing the db.add() we did earlier), closes the database session, and returns a message indicating that the time slot is already booked.
    
    db_appointment = create_new_appointment(db, appointment, user_id) # creates a SQLAlchemy ORM object. This is like a Python representation of a row in the appointments table.

    print(appointment)
    return {
        "message": "Appointment received",
        "data": db_appointment.service_id # return the id of the new appointment
    }


# @router.get("/appointments")
# def get_appointments(db: Session = Depends(get_db)):
#     """
#     Get all appointments from the database and return them as a list.
#     """
#     appointments = db.query(Appointment).all() # this is how you query the database with SQLAlchemy. It translates to "SELECT * FROM appointments" in SQL. The result is a list of Appointment objects.
#     return [
#         {
#             "id": appointment.id,
#             "name": appointment.name,
#             "phone_number": appointment.phone_number,
#             "service_id": appointment.service_id,
#             "notes": appointment.notes,
#             "date": appointment.date
#         }

#         for appointment in appointments
#     ]

@router.get("/appointments", response_model=list[AppointmentResponse]) # 📋 Declare your output schema shape
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    
    return appointments #Return the raw rows directly!


@router.get("/appointments/{user_id}")
def get_appointments_by_user(user_id: int, db: Session = Depends(get_db), response_model = list[AppointmentResponse]):
    """
    Get all appointments for a specific user from the database and return them as a list. The user_id is passed in the URL, and FastAPI automatically converts it to an integer because we specified user_id: int.
    """
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all() # this translates to "SELECT * FROM appointments WHERE user_id = {user_id}" in SQL. The result is a list of Appointment objects that match the user_id.
    return appointments


# @router.get("/my-appointments")
# def get_my_appointments(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
#     """
#     Get all appointments for the currently logged in user. This endpoint expects an Authorization header with a JWT token, which it decodes to get the user_id, and then queries the database for appointments with that user_id.
#     """

#     appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
#     return [
#         {
#             "id": appointment.id,
#             "name": appointment.name,
#             "phone_number": appointment.phone_number,
#             "service": appointment.service,
#             "notes": appointment.notes,
#             "date": appointment.date

#         }

#         for appointment in appointments
#     ]

@router.get("/my-appointments", response_model=list[AppointmentResponse]) # 📋 Declare your output schema shape
def get_my_appointments(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
    
    return appointments # Return the raw rows directly!


@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    delete an appointment from the database by id. The appointment_id is passed in the URL, and FastAPI automatically converts it to an integer because we specified appointment_id: int.
    """

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first() # this translates to "SELECT * FROM appointments WHERE id = {appointment_id} LIMIT 1" in SQL. It returns the first appointment that matches the id, or None if no appointment is found.
    message = delete_db(db, appointment)
    

    return {"message": message}


@router.delete("/my-appointments/{appointment_id}")
def user_delete_appointment(appointment_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """
    delete an appointment from the database by id, but only if it belongs to the currently logged in user. This endpoint expects an Authorization header with a JWT token, which it decodes to get the user_id, and then checks if the appointment with the given id has that user_id before deleting it.
    """

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == user_id).first() # this translates to "SELECT * FROM appointments WHERE id = {appointment_id} AND user_id = {user_id} LIMIT 1" in SQL. It returns the first appointment that matches the id and belongs to the user, or None if no appointment is found.
    message = delete_db(db, appointment)

    return {"message": message}


@router.get("/appointments/slots/{date}")
def get_available_slots(date: str, db: Session = Depends(get_db)):
    """
    This endpoint returns the available time slots for a given date. It checks the appointments in the database for that date and returns the hours that are not booked.
    """
    booking_slots = constants.BOOKING_SLOTS.copy() # this is a list of hours that we want to offer for booking, defined in config/constants.py

    for slot in booking_slots:
        time_slot = datetime.strptime(
            f"{date} {slot}",
            "%Y-%m-%d %H:%M") # this constructs a datetime string for the given date and slot hour, like "2024-07-01 09:00:00"
        appointment = db.query(Appointment).filter(Appointment.date == time_slot).first() #
        booking_slots[slot] = appointment is None # if there's an appointment at that time slot, it means it's not available, so we set it to False. If there's no appointment, it means it's available, so we set it to True.
        
    return booking_slots

@router.get("/appointments/services/{id}")
def parse_service_id(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_service = db.query(Service).get(appointment.service_id)
    return {
        "service_name": db_service.name,
        "service_price": db_service.price,
        "service_description": db_service.description
    }



