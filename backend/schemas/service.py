from pydantic import BaseModel
from typing import Optional

#Data needed to create a new service (e.g., admin dashboard)
class ServiceCreate(BaseModel):
    name: str
    price: int
    description: Optional[str] = None

#Data sent back to the frontend (e.g., your catalog page)
class ServiceResponse(BaseModel):
    id: int          # 🔢 Generated automatically by the database table
    name: str
    price: int
    description: Optional[str]

    class Config:
        from_attributes = True  # 🔄 Allows Pydantic to read SQLAlchemy rows smoothly