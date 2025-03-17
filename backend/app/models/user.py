import uuid
from pydantic import BaseModel, EmailStr, Field
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
    role: UserRole
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"  # Collection name in MongoDB

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }