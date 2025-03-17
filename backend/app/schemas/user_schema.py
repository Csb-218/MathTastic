from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from app.models.user import User

class UserCreate(BaseModel):
    name: str
    email: EmailStr  # Using EmailStr for better email validation
    role: UserRole
    uid:str

class UserLogin(BaseModel):
    email: EmailStr
    uid: str

class LoginResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"