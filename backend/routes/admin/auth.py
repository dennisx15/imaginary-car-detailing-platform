from tokenize import String

from fastapi import APIRouter, Depends, Header, HTTPException
from backend.schemas.appointment import AppointmentCreate, AppointmentResponse
from passlib.context import CryptContext

from backend.database.connection import SessionLocal
from backend.database.models import Appointment, Service

from backend.config import constants
from datetime import datetime

from backend.schemas.tokens import TokenResponse
from backend.utils.security import *
from sqlalchemy.orm import Session

#need to set a secret key and algorithm for JWT token generation. In a real application, you should use a strong, random secret key and keep it safe (not hardcoded in your code). For simplicity, we'll just use a hardcoded string here.
SECRET_KEY = constants.SECRET_KEY
ALGORITHM = constants.ALGORITHM

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    This endpoint is for logging in. It checks if a user with the given email exists, and if the password is correct. In a real application, you would also generate and return a JWT token here, but for simplicity, we'll just return a success message if the login is successful.
    """
    db_user = db.query(User).filter(User.email == user.email).first() # query the database for a user with the given email. This translates to "SELECT * FROM users WHERE email = {user.email} LIMIT 1" in SQL. The result is a User object or None if no user is found.


    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Match credentials
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")
        
    # THE SECURE BLOCK: Raise a true 403 Forbidden network error.
    if not db_user.is_verified:
        raise HTTPException(
            status_code=403, 
            detail="Please verify your email address before logging in."
        )
    
    if not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    
    token = create_access_token(
    db_user.id)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        is_admin=db_user.is_admin
    )
