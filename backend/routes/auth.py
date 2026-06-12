from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from backend.database.connection import SessionLocal
from backend.schemas.tokens import TokenResponse
from backend.schemas.user import UserCreate, UserLogin, UserRegister, UserResponse
from backend.database.models import User
from jose import jwt, JWTError, ExpiredSignatureError
from backend.config import constants

from backend.utils.email import send_verification_email
from backend.utils.security import *


#need to set a secret key and algorithm for JWT token generation. In a real application, you should use a strong, random secret key and keep it safe (not hardcoded in your code). For simplicity, we'll just use a hardcoded string here.
SECRET_KEY = constants.SECRET_KEY
ALGORITHM = constants.ALGORITHM

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)



@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Look for pre-existing records...
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="An account is already registered under this email.")

    # 2. Add the unverified user profile row to the database...
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        is_verified=False # Locked until they click!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate the temporary token signatures (from our security utils)
    token = create_access_token(new_user.id)

    # Construct the target verification address url string
    # (Pointing straight to the callback validation route we written earlier!)
    verification_link = f"{constants.API_BASE_URL}/verify-email?token={token}"
    #verification_link = f"http://127.0.0.1:8000/verify-email?token={token}"

    # Dispatch the verification message packet
    send_verification_email(new_user.email, verification_link)

    return new_user

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
    token = create_access_token(
    db_user.id)

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    This endpoint is for verifying the user's email. It expects a token in the query parameters, which it decodes to get the user_id, and then updates the corresponding user in the database to set is_verified to True.
    """
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()

    redirect_url = f"{constants.FRONTEND_BASE_URL}/verification_success.html"
    return RedirectResponse(url=redirect_url) # Redirect the user to a frontend page that says "Email verified successfully!" or something like that. You would need to create this page in your frontend assets.