from pydantic import BaseModel, Field, constr
from typing import List, Optional
from app.models.activity import Activity
from app.models.user import User
 
class GameBase(BaseModel):
    title: constr(max_length=50)

class GameCreate(GameBase):
    creator_id: str
    activity_ids: List[str] = []  # Accept IDs in request
    template: Optional[bool] = False

class GameUpdate(BaseModel):
    title: Optional[constr(max_length=50)] = None
    activity_ids: Optional[List[str]] = None  # Accept IDs in update request
    template: Optional[bool] = False

class GameResponse(BaseModel):
    id: str
    title: str
    creator: str
    activities: List[Activity]  # Return full activities
    target_range: List[int]
    max_time_allowed: int
    total_points: int
    template: bool

    class Config:
        from_attributes = True