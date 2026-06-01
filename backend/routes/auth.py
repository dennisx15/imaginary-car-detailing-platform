from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from backend.database.connection import SessionLocal
from backend.schemas.user import UserCreate, UserLogin, UserRegister
from backend.database.models import User
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from backend.config import constants


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


@router.post("/register")
def register(user: UserRegister):
    """
    register a new user. This endpoint expects a JSON object with an email and password, hashes the password, and stores the new user in the database.
    """

    db = SessionLocal()
    try:
        hashed_password = hash_password(
        user.password
    )
        new_user = User(
        email=user.email,
        password_hash=hashed_password
    ) # create a new User object with the email and hashed password. This is a SQLAlchemy ORM object that represents a row in the users table.
        db.add(new_user) # tell SQLAlchemy to track this new user for insertion into the database.
        db.commit() # this is when the SQL INSERT statement is actually sent to the database. The new user is now stored in the database.

        return {
        "message": "User created"
        }
    except Exception as e:
        db.rollback() # if there's an error (like a duplicate email), we rollback the transaction to undo any changes.
        raise HTTPException(
            status_code=400,
            detail="Error creating user")


@router.post("/login")
def login(user: UserLogin):
    """
    This endpoint is for logging in. It checks if a user with the given email exists, and if the password is correct. In a real application, you would also generate and return a JWT token here, but for simplicity, we'll just return a success message if the login is successful.
    """
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first() # query the database for a user with the given email. This translates to "SELECT * FROM users WHERE email = {user.email} LIMIT 1" in SQL. The result is a User object or None if no user is found.

    if not db_user:
        return {
            "message": "Invalid email or password"
        }

    if not pwd_context.verify(user.password, db_user.password_hash):
        return {
            "message": "Invalid email or password"
        }
    token = create_access_token(
    db_user.id)

    return {

    "access_token": token,

    "token_type": "bearer" # this is a convention to indicate that the token is a bearer token, which means the client should include it in the Authorization header of future requests like "Authorization: Bearer {token}"
    }

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