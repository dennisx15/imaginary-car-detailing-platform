import os
import string
from dotenv import load_dotenv


BOOKING_SLOTS = {
    "09:00": True,
    "10:00": True,
    "11:00": True,
    "12:00": True,
    "13:00": True,
    "14:00": True,
    "15:00": True,
    "16:00": True,
    "17:00": True
}

load_dotenv() #load .env to access the values in there

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")
