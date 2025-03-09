from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.user import User
from app.schemas.user_schema import UserCreate


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[User])
async def get_users():
    users = await User.find_all().to_list()
    return users

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