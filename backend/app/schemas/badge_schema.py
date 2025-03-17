from pydantic import BaseModel, Field
from typing import Optional, Literal

class BadgeBase(BaseModel):
    badge_name: Literal[
        "Beginner",
        "QuickGrasper",
        "Learner",
        "SelfLearner",
        "Master",
        "Prodigy",
        "Genius"
    ]
    points_to_badge: int = Field(
        ge=100,
        le=2000,
        description="Points required to achieve this badge"
    )

class BadgeCreate(BadgeBase):
    pass

class BadgeUpdate(BaseModel):
    points_to_badge: int = Field(
        ge=100,
        le=2000,
        description="Points required to achieve this badge"
    )

class BadgeResponse(BadgeBase):
    id: str

    class Config:
        from_attributes = True