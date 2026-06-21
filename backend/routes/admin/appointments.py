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

@router.get("/appointments", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id_admin)):
    """
    Get all appointments from the database and return them as a list.
    """
    appointments = db.query(Appointment).all()
    return appointments #Return the raw rows directly!



@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id_admin)):
    """
    delete an appointment from the database by id. The appointment_id is passed in the URL, and FastAPI automatically converts it to an integer because we specified appointment_id: int.
    """

    #TODO: Handle edge case where appointment_id doesn't exist. Right now it just returns "Appointment deleted successfully" even if the id is invalid. We should check if the appointment exists before trying to delete it, and return a 404 error if it doesn't exist.
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first() # this translates to "SELECT * FROM appointments WHERE id = {appointment_id} LIMIT 1" in SQL. It returns the first appointment that matches the id, or None if no appointment is found.
    message = delete_db(db, appointment)
    

    return {"message": message}
