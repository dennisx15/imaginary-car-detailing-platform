from sqlalchemy.orm import DeclarativeBase # 
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models. All models should inherit from this class.
    """
    pass


class Appointment(Base):

    __tablename__ = "appointments" # create an SQL table called appointments

    id = Column(Integer, primary_key=True, index=True) # defines columns. Creates integer column, primary key, indexed

    # these columns will store the name and service of the appointment
    name = Column(String)
    phone_number = Column(String)
    service = Column(String)
    notes = Column(String)
    user_id = Column(Integer) # this will store the id of the user who made the appointment. It's an integer that references the id column in the users table.

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)