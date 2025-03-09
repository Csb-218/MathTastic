from beanie import Document, Link
from typing import List,Optional
from pydantic import Field
from .user import User
from .game import Game
from .badge import Badge
from .activity import Activity

class Progress(Document):
    student: Link[User] = Field(
        ...,
        description="Reference to the student user"
    )
    
    games_completed: List[Link[Game]] = Field(
        default_factory=list,
        description="List of completed games"
    )
    
    badges: List[Link[Badge]] = Field(
        default_factory=list,
        description="List of earned badges"
    )
    
    points_earned: int = Field(
        default=0,
        ge=0,
        description="Total points accumulated from completed games"
    )
    
    active_game: Optional[Link[Game]] = Field(
        default=None,
        description="Reference to currently active game"
    )
    
    current_game_level: Optional[int] = Field(
        default=None,
        ge=1,
        description="Current level in active game"
    )
    
    active_activity: Optional[Link[Activity]] = Field(
        default=None,
        description="Reference to current activity in active game"
    )

    class Settings:
        name = "progress"
        indexes = [
            "student",
            "points_earned"
        ]

    async def update_points(self) -> None:
        """Updates total points based on completed games."""
        total_points = 0
        for game_link in self.games_completed:
            game = await game_link.fetch()
            if game:
                total_points += game.total_points
        
        self.points_earned = total_points
        await self.update_badges()

    async def update_badges(self) -> None:
        """Updates badges based on points earned."""
        all_badges = await Badge.find().sort("points_to_badge").to_list()
        earned_badges = []

        for badge in all_badges:
            if self.points_earned >= badge.points_to_badge:
                earned_badges.append(Link(badge, Badge))
            else:
                break

        self.badges = earned_badges
        await self.save()

    @classmethod
    async def create_progress(cls, student: User) -> 'Progress':
        """Creates a new progress record for a student."""
        progress = cls(
            student=Link(student),
            games_completed=[],
            badges=[],
            points_earned=0
        )
        await progress.insert()
        return progress

    async def add_completed_game(self, game: Game) -> None:
        """Adds a completed game and updates points and badges."""
        if Link(game) not in self.games_completed:
            self.games_completed.append(Link(game, Game))
            await self.update_points()
            await self.save()