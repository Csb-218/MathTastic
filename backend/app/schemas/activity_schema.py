from pydantic import BaseModel, Field
from typing import List, Optional

class ActivityBase(BaseModel):
    level: int = Field(default=1, ge=1)
    target: int = Field(...)
    addends: List[int] = Field(default_factory=list)
    addends_size: int = Field(...)
    time_limit: Optional[int] = None
    hints: Optional[List[str]] = None
    points: int = Field(default=10, ge=0)
    success_feedback: str = Field(default="Great job!")
    failure_feedback: str = Field(default="Try again!")

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    level: int = Field(ge=1, description="Level must be greater than or equal to 1")
    target: int = Field(ge=0, description="Target must be non-negative")
    addends: List[int] = Field(
        default_factory=list,
        description="List of numbers to be added"
    )
    addends_size: int = Field(ge=1, description="Must have at least 1 addend")
    time_limit: int = Field(ge=0, description="Time limit must be non-negative")
    hints: Optional[List[str]] = None
    points: int = Field(ge=0, description="Points must be non-negative")
    success_feedback: str = Field(min_length=1)
    failure_feedback: str = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "level": 2,
                "target": 10,
                "addends": [5, 5],
                "addends_size": 2,
                "time_limit": 30,
                "hints": ["Think about pairs that add up to 10"],
                "points": 10,
                "success_feedback": "Great job!",
                "failure_feedback": "Try again!"
            }
        }

class ActivityResponse(BaseModel):
    id: str
    level: int
    target: int
    addends: List[int]
    addends_size: int
    time_limit: Optional[int]
    hints: Optional[List[str]]
    points: int
    success_feedback: str
    failure_feedback: str

    class Config:
        from_attributes = True