from fastapi import APIRouter, HTTPException
from app.models.user import User, UserRole
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.controllers.userControllers import get_users


# Create a Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[User])
async def getUser():
    return await get_users()



@router.post("/", response_model=User)
async def add_user(user: UserCreate):
    try:
        # Create new user document
        new_user = User(
            name=user.name,
            email=user.email,
            password=user.password,  # Note: In production, hash the password
            role=user.role,
            created_at=datetime.utcnow()
        )
        # Save to database
        await new_user.insert()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))