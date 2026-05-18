from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base


DATABASE_URL = "postgresql://postgres:ZZqq112233@localhost:5432/car_detailer_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine) # Create all tables defined from Base subclasses.