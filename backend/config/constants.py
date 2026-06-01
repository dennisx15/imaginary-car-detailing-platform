
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

SECRET_KEY = "super_secret_key" # In a real application, you should use a strong, random secret key and keep it safe (not hardcoded in your code). For simplicity, we'll just use a hardcoded string here.
ALGORITHM = "HS256"
DATABASE_URL = "postgresql://postgres:ZZqq112233@localhost:5432/car_detailer_db" # this is the connection string for our PostgreSQL database. It includes the username (postgres), password (ZZqq112233), host (localhost), port (5432), and database name (car_detailer_db). In a real application, you should use environment variables to store sensitive information like database credentials instead of hardcoding them in your code.
