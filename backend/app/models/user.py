import uuid
from pydantic import BaseModel, EmailStr
from beanie import Document, Indexed
from enum import Enum
from datetime import datetime
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "admin"
    EDUCATOR = "educator"
    STUDENT = "student"

class User(Document):
    name: str
    email: Indexed(str, unique=True)  # Indexed for faster queries and unique constraint
    password: str
    role: UserRole
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"  # Collection name in MongoDB

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }