from fastapi import Header, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from backend.config.constants import SECRET_KEY, ALGORITHM
from backend.database.connection import SessionLocal
from backend.database.models import Appointment
from backend.schemas.appointment import AppointmentCreate
from sqlalchemy.orm import Session


def check_existing_appointment(db, appointment_date):
    """Checks if a time slot is already taken."""
    return db.query(Appointment).filter(Appointment.date == appointment_date).first()

def create_new_appointment(db, appointment: AppointmentCreate, user_id: int):
    """Saves a brand new appointment row to the database."""
    db_appointment = Appointment(
        name=appointment.name,
        service_id=appointment.service_id,
        phone_number=appointment.phone_number,
        notes=appointment.notes,
        date=appointment.date,
        user_id=user_id
    )
    db.add(db_appointment) # tells SQLAlchemy: “track this object for insertion.” notthing is actually sent to the database yet.
    db.commit() # this is when the SQL INSERT statement is actually sent to the database. The new appointment is now stored in the database.
    db.refresh(db_appointment) # reloads object from database. Because PostgreSQL automatically generates an id for new rows, this is how we get the generated id back into our db_appointment object.
    return db_appointment

def decode_token(token: str):
    """
    function for decoding a token. also checks if the token is valid and not expired. If the token is valid, it returns the payload (which contains the user_id). If the token is invalid or expired, it raises an HTTPException with a 401 status code.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

def get_current_user_id(authorization: str = Header(None)) -> int:
    """
    A reusable dependency that intercepts requests, extracts the JWT,
    validates it, and returns the authenticated user's ID.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
        
    try:
        # 1. Split 'Bearer <token>' to get the raw token string
        token = authorization.split(" ")[1]
        
        # 2. Decode the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
            
        return user_id
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_db():
    db = SessionLocal() # 1. Open the session before the route runs
    try:
        yield db        # 2. Hand the clean connection over to the route. Yield pauses the function until the route is done, then resumes to execute the finally block.
    finally:
        db.close()      # 3. Close the session after the route completes


def delete_db(db: Session, appointment):
    if appointment:
        db.delete(appointment)
        db.commit()
        message = "Appointment deleted"
    else:
        message = "Appointment not found or does not belong to user"
    return message
