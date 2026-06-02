from sqlalchemy.orm import DeclarativeBase, relationship # 
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models. All models should inherit from this class.
    """
    pass


class Appointment(Base):
    """
This class defines the structure of the appointments table in the database. Each instance of this class represents a row in the appointments table, and each attribute corresponds to a column in the table.
    """

    __tablename__ = "appointments" # create an SQL table called appointments

    id = Column(Integer, primary_key=True, index=True) # defines columns. Creates integer column, primary key, indexed

    # these columns will store the name and service of the appointment
    name = Column(String)
    phone_number = Column(String)
    notes = Column(String)
    date = Column(DateTime) # this will store the date and time of the appointment. DateTime is a special type that can store both date and time information.
    user_id = Column(Integer) # this will store the id of the user who made the appointment. It's an integer that references the id column in the users table.

    service_id = Column(Integer, ForeignKey("services.id"), nullable=False) # this will store the id of the service that the user selected for the appointment. It's an integer that references the id column in the services table.
    service = relationship("Service")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)#Primary key for the users table, unique identifier for each user. increments by 1 each time a user is added
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)