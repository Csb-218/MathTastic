from fastapi import APIRouter, HTTPException, Path
from app.models.game import Game
from app.models.activity import Activity
from app.models.user import User
from app.schemas.game_schema import GameCreate, GameUpdate, GameResponse
from beanie import Link
from typing import List
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

def validate_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@router.get("/", response_model=List[GameResponse])
async def get_games():
    try:
        games = await Game.find_all(fetch_links=True).to_list()
        return [
            GameResponse(
            id=str(game.id),
            title=game.title,
            creator=str(game.creator.id),
            activities=[(activity) for activity in game.activities],
            target_range=game.target_range,
            max_time_allowed=game.max_time_allowed,
            total_points=game.total_points,
            template=game.template
        )
            for game in games
        ]
    except Exception as e:
        print(f"Error retrieving games: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: str = Path(..., description="The ID of the game to get")):
    object_id = validate_object_id(game_id)
    game = await Game.get(object_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameResponse(
        id=str(game.id),
        title=game.title,
        creator_id=str(game.creator.id),
        activity_ids=[str(activity.id) for activity in game.activities],
        target_range=game.target_range,
        max_time_allowed=game.max_time_allowed,
        total_points=game.total_points
    )

@router.post("/create", response_model=GameResponse)
async def create_game(game_data: GameCreate):
    try:
        # Verify user exists
        creator_id = validate_object_id(game_data.creator_id)
        creator = await User.get(creator_id)
        if not creator:
            raise HTTPException(status_code=404, detail="Creator not found")

        # Create new game first
        new_game = Game(
            title=game_data.title,
            creator=Link(creator_id, User),
            template=game_data.template
        )
        await new_game.insert()

        # Create activities with reference to the game
        for activity_data in game_data.activities:
            activity = Activity(
                **activity_data.dict(),
                game=Link(new_game.id, Game)
            )
            await activity.insert()

        # Update game statistics
        await new_game.update_stats()
        await new_game.save()

        return GameResponse(
            id=str(new_game.id),
            title=new_game.title,
            creator_id=str(new_game.creator.id),
            activities=await Activity.find({"game.id": new_game.id}).to_list(),
            target_range=new_game.target_range,
            max_time_allowed=new_game.max_time_allowed,
            total_points=new_game.total_points,
            template=new_game.template
        )

    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{game_id}/update", response_model=GameResponse)
async def update_game(
    game_id: str = Path(..., description="The ID of the game to update"),
    game_update: GameUpdate = None
):
    object_id = validate_object_id(game_id)
    game = await Game.get(object_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        if game_update.title:
            game.title = game_update.title

        if game_update.template:
            game.template = game_update.template
        
        if game_update.activity_ids:
            activities = []
            for activity_id in game_update.activity_ids:
                object_id = validate_object_id(activity_id)
                activity = await Activity.get(object_id)
                if not activity:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Activity with id {activity_id} not found"
                    )
                activities.append(activity)  # Store full activity document
            game.activities = activities
            await game.update_stats()
        
        await game.save()
        return GameResponse(
            id=str(game.id),
            title=game.title,
            creator=str(game.creator),
            activities=game.activities,  # Return full activities
            target_range=game.target_range,
            max_time_allowed=game.max_time_allowed,
            total_points=game.total_points,
            template=game.template
        )
    except Exception as e:
        print(f"Error updating game: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{game_id}")
async def delete_game(game_id: str):
    game = await Game.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    await game.delete()
    return {"message": "Game deleted successfully"}