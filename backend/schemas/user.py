from pydantic import BaseModel

class UserCreate(BaseModel):

    email: str #EmailStr validates that the incoming text matches a true email format (e.g., name@domain.com)
    password: str

class UserRegister(BaseModel):

    email: str #EmailStr validates that the incoming text matches a true email format (e.g., name@domain.com)
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_verified: bool
    is_admin: bool
    is_employee: bool

    class Config:
        from_attributes = True #Allows Pydantic to read raw database rows automatically