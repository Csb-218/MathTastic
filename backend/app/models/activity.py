from beanie import Document,Link
from typing import List, Optional
from pydantic import Field

class Activity(Document):
    level: int = Field(default=1, ge=1)
    target: int = Field(...)  # required field
    addends: List[int] = Field(default_factory=list)
    addends_size: int = Field(...)
    time_limit: Optional[int] = None
    hints: Optional[List[str]] = None
    points: int = Field(default=10, ge=0)
    success_feedback: str = Field(default="Great job!")
    failure_feedback: str = Field(default="Try again!")


    class Settings:
        name = "activities"  # Collection name in MongoDB
        indexes = [
            "game",  # Add index for game reference
            "level"
        ]
        
    class Config:
        json_schema_extra = {
            "example": {
                "level": 1,
                "target": 10,
                "addends": [5, 5],
                "addends_size": 2,
                "time_limit": 30,
                "hints": ["Think about pairs that add up to 10"],
                "points": 10,
                "success_feedback": "Excellent! You found the correct combination!",
                "failure_feedback": "Don't worry, keep practicing!"
            }
        }