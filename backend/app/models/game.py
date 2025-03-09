from beanie import Document, Link
from typing import List
from pydantic import Field, constr
from .activity import Activity
from .user import User 

class Game(Document):
    title: constr(max_length=50) = Field(..., description="Game title, max 50 characters")
    creator: Link[User] = Field(..., description="Reference to creator user")
    # activities: List[Link[Activity]] = Field(  # Changed to store Links
    #     default_factory=list,
    #     description="List of activity references"
    # )
    target_range: List[int] = Field(
        default_factory=lambda: [0, 0],
        min_items=2,
        max_items=2,
        description="Range of target values [min, max]"
    )
    max_time_allowed: int = Field(
        default=0,
        ge=0,
        description="Maximum time limit among all activities"
    )
    total_points: int = Field(
        default=0,
        ge=0,
        description="Sum of points from all activities"
    )
    template: bool = Field(
        default=False,
        description="Flag to indicate if game is a template"
    )

    class Settings:
        name = "games"
        indexes = [
            "title",
            "creator",
            "target_range"
        ]

    async def update_stats(self):
        """Update game statistics based on linked activities."""
        if not self.activities:
            self.target_range = [0, 0]
            self.max_time_allowed = 0
            self.total_points = 0
            return

        try:
            targets = []
            max_time = 0
            total_points = 0

            for activity in self.activities:
                print(1,activity)  # Fetch activity from reference
                if activity.target is not None:
                    targets.append(activity.target)
                if activity.time_limit is not None:
                    max_time = max(max_time, activity.time_limit)
                if activity.points is not None:
                    total_points += activity.points

            self.target_range = [min(targets) if targets else 0, max(targets) if targets else 0]
            self.max_time_allowed = max_time
            self.total_points = total_points

        except Exception as e:
            print(f"Error updating game stats: {e}")
            self.target_range = [0, 0]
            self.max_time_allowed = 0
            self.total_points = 0
            raise e

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Addition Adventure Level 1",
                "creator": "user_id_here",
                "activities": ["activity_id_1", "activity_id_2"],
                "target_range": [5, 20],
                "max_time_allowed": 60,
                "total_points": 50,
                "template": False
            }
        }