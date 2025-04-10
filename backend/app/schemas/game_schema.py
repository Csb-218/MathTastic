from pydantic import BaseModel, Field, constr
from typing import List, Optional , Literal
from app.models.activity import Activity
from app.models.user import User
 
class GameBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=50)
    description: Optional[str] = Field(...,min_length=20, max_length=200)

class GameCreate(GameBase):
    creator_id: str
    activity_ids: List[str] = []  # Accept IDs in request
    template: Optional[bool] = False
    difficulty: Literal['easy', 'medium', 'hard'] = Field(
        default='easy',
        description="Difficulty level of the game (easy, medium, or hard)"
    )
    age_range: str = Field(
        default="5-10",
        max_length=5,
        description="Age range for the game, max 5 characters"
    )


class GameUpdate(BaseModel):
    title:  str = Field(..., min_length=5, max_length=50)
    description: Optional[str] = Field(None, min_length=20, max_length=200)
    activity_ids: Optional[List[str]] = None  # Accept IDs in update request
    template: Optional[bool] = False
    difficulty: Optional[Literal['easy', 'medium', 'hard']] = Field(
        default='easy',
        description="Difficulty level of the game (easy, medium, or hard)"
    )
    age_range: Optional[str] = Field(
        default="5-10",
        max_length=5,
        description="Age range for the game, max 5 characters"
    )

class AddActivities(BaseModel):
    """Schema for adding activities to a game"""
    activity_ids: List[str] = Field(
        default_factory=list,
        description="List of activity IDs to add to the game"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "activity_ids": ["activity_id_1", "activity_id_2"]
            }
        }

class GameResponse(BaseModel):
    id: str
    description: str
    title: str
    creator: str
    activities: List[Activity]
    age_range: str
    difficulty:Literal['easy', 'medium', 'hard']
    target_range: List[int]
    max_time_allowed: int
    total_points: int
    template: bool

    class Config:
        from_attributes = True