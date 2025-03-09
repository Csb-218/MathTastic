from pydantic import BaseModel, Field
from beanie import Document, Link
from typing import List, Optional
from app.models.activity import Activity
from app.models.badge import Badge
from app.models.game import Game

class ProgressBase(BaseModel):
    student_id: str = Field(..., description="ID of the student")
    games_completed: List[str] = Field(
        default_factory=list,
        description="List of completed game IDs"
    )
    badges: List[str] = Field(
        default_factory=list,
        description="List of earned badge IDs"
    )
    points_earned: int = Field(
        default=0,
        ge=0,
        description="Total points accumulated"
    )
    active_game: Optional[str] = Field(
        default=None,
        description="ID of the currently active game"
    )
    current_game_level: Optional[int] = Field(
        default=None,
        ge=1,
        description="Current level in active game"
    )
    active_activity: Optional[str] = Field(
        default=None,
        description="ID of current activity in active game"
    )

class ProgressCreate(ProgressBase):
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "67cab65c42855334da38a504",
                "games_completed": [],
                "badges": [],
                "points_earned": 0,
                "active_game": None,
                "current_game_level": None,
                "active_activity": None
            }
        }

class ProgressUpdate(BaseModel):
    games_completed: Optional[List[str]] = None
    active_game: Optional[str] = None
    current_game_level: Optional[int] = Field(None, ge=1)
    active_activity: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "active_game": "67cb440691f1f65e84f32b77",
                "current_game_level": 1,
                "active_activity": "67cad8c6c536441714a5c4c5"
            }
        }

class ProgressResponse(BaseModel):
    id: str
    student_id: str
    games_completed: List[str]
    badges: List[str]
    points_earned: int
    active_game: Optional[str] = None
    current_game_level: Optional[int] = None
    active_activity: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "67cb440691f1f65e84f32b77",
                "student_id": "67cab65c42855334da38a504",
                "games_completed": ["67cb440691f1f65e84f32b77"],
                "badges": ["67cad8c6c536441714a5c4c5"],
                "points_earned": 100,
                "active_game": "67cb440691f1f65e84f32b77",
                "current_game_level": 1,
                "active_activity": "67cad8c6c536441714a5c4c5"
            }
        }