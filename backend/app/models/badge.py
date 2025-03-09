from beanie import Document, Indexed
from typing import Literal
from pydantic import Field

class Badge(Document):
    badge_name: Literal[
        "Beginner",
        "QuickGrasper",
        "Learner",
        "SelfLearner",
        "Master",
        "Prodigy",
        "Genius"
    ] = Field(
        ...,
        description="Badge level name"
    )
    
    points_to_badge: int = Field(
        ...,
        ge=100,  # minimum points
        le=2000,  # maximum points
        description="Points required to achieve this badge"
    )

    class Settings:
        name = "badges"
        indexes = [
            "badge_name",
            "points_to_badge"
        ]

    @classmethod
    def get_badge_thresholds(cls) -> dict:
        """Returns the mapping of badge names to their point thresholds."""
        return {
            "Beginner": 100,
            "QuickGrasper": 300,
            "Learner": 500,
            "SelfLearner": 800,
            "Master": 1000,
            "Prodigy": 1500,
            "Genius": 2000
        }

    @classmethod
    async def determine_badge(cls, points: int) -> str:
        """Determines the appropriate badge name based on points."""
        thresholds = cls.get_badge_thresholds()
        earned_badge = "Beginner"
        
        for badge, threshold in thresholds.items():
            if points >= threshold:
                earned_badge = badge
            else:
                break
                
        return earned_badge