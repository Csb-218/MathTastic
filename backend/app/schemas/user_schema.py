from app.models.user import UserRole
from pydantic import BaseModel

# Create a Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole