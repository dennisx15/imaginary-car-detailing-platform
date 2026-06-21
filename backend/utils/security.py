from datetime import datetime, timedelta
from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from backend.config.constants import SECRET_KEY, ALGORITHM
from backend.database.connection import SessionLocal
from backend.database.models import Appointment, User
from backend.schemas.appointment import AppointmentCreate
from sqlalchemy.orm import Session

from backend.schemas.user import UserRegister, UserResponse, UserLogin


def check_existing_appointment(db, appointment_date):
    """Checks if a time slot is already taken."""
    return db.query(Appointment).filter(Appointment.date == appointment_date).first()

def check_existing_account(db, user: UserRegister):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="An account is already registered under this email address."
        )

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

def create_access_token(user_id: int):

    payload = {

        "user_id": user_id,

        "exp": datetime.utcnow() + timedelta(hours=1) # token expires in 1 hour
        
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    ) # this generates a JWT token with the user_id and expiration time in the payload, signed with the secret key and algorithm we defined earlier.

    return token

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
        ) # checks if the token has been tampered with or is otherwise invalid. If the token is valid but has expired, it raises a different error indicating that the token has expired.

def get_current_user_id(authorization: str = Header(None), check_admin: bool = False) -> int:
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
            
        if check_admin:
            # Check if the user is an admin
            if not payload.get("is_admin"):
                raise HTTPException(status_code=403, detail="Access denied")

        return user_id
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_id_admin(authorization: str = Header(None)) -> int:
    """
    A wrapper around get_current_user_id that specifically checks for admin privileges.
    """
    return get_current_user_id(authorization, check_admin=True)

    
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


