from typing import List
from fastapi import APIRouter, HTTPException, Path, Body
from app.models.game import Game
from app.models.activity import Activity
from app.models.user import User
from app.schemas.game_schema import GameCreate, GameUpdate, GameResponse, AddActivities
from app.utils.helpers import validate_object_id

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[GameResponse])
async def get_games():
    try:
        # Fetch all games with linked documents
        games = await Game.find_all().to_list()
        
        responses = []
        for game in games:
            # Ensure activities are fetched
            activities = []
            for activity_link in game.activities:
                activity = await Activity.get(activity_link.id)
                if activity:
                    activities.append(activity)
            
            # Create response with fetched activities
            game_response = GameResponse(
                id=str(game.id),
                title=game.title,
                description=game.description,
                creator=str(game.creator),
                age_range=game.age_range,
                difficulty=game.difficulty,
                activities=activities,  # Use fetched activities
                target_range=game.target_range,
                max_time_allowed=game.max_time_allowed,
                total_points=game.total_points,
                template=game.template
            )
            responses.append(game_response)
            
        return responses

    except Exception as e:
        print(f"Error retrieving games: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: str = Path(..., description="The ID of the game to get")):

    game = await Game.get(str(validate_object_id(game_id,"game_id")),fetch_links=True)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return  GameResponse(
            id=str(game.id),
            title=game.title,
            description=game.description,
            creator=str(game.creator.id),
            age_range=game.age_range,
            difficulty=game.difficulty,
            activities=list(game.activities),
            target_range=game.target_range,
            max_time_allowed=game.max_time_allowed,
            total_points=game.total_points,
            template=game.template
        )

@router.post("/create", response_model=GameResponse)
async def create_game(game_data: GameCreate) -> GameResponse:
    try:
        # Verify user exists 
        creator = await User.get(validate_object_id(game_data.creator_id, "creator_id"))
        if not creator:
            raise HTTPException(status_code=404, detail="Creator not found")

        # Create new game first
        new_game = Game(
            title=game_data.title,
            creator=creator,
            template=game_data.template
        )
        await new_game.insert()

        # Create activity references
        activities = []
        for activity_id in game_data.activity_ids:
            activity_id = validate_object_id(activity_id, "activity_id")
            activity = await Activity.get(activity_id)
            if not activity:
                raise HTTPException(status_code=404, detail=f"Activity with id {activity_id} not found")
            activities.append(activity)

        new_game.activities = activities
        await new_game.update_stats()
        await new_game.save()

        return GameResponse(
            id=str(new_game.id),
            title=new_game.title,
            description=new_game.description,
            creator=str(new_game.creator_id),
            age_range=new_game.age_range,
            difficulty=new_game.difficulty,
            activities=[activity for activity in new_game.activities],
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
    game = await Game.get(validate_object_id(game_id, "game_id"))
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        if game_update.title:
            game.title = game_update.title

        if game_update.template is not None:
            game.template = game_update.template

        if game_update.description:
            game.description = game_update.description

        if game_update.age_range:
            game.age_range = game_update.age_range

        if game_update.difficulty:
            game.difficulty = game_update.difficulty
        
        if game_update.activity_ids:
            # Create new activities list with full Activity instances
            activities = []
            for activity_id in game_update.activity_ids:
                activity = await Activity.get(validate_object_id(activity_id, "activity_id"))
                if not activity:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Activity with id {activity_id} not found"
                    )
                # Add the Activity instance directly
                activities.append(activity)
            
            # Update game's activities and stats
            game.activities = activities
            await game.update_stats()
        
        # Save changes
        await game.save()
        
        # Fetch fresh game to ensure all data is properly loaded
        updated_game = await Game.get(game.id, fetch_links=True)

        return GameResponse(
            id=str(updated_game.id),
            title=updated_game.title,
            description=updated_game.description,
            age_range=updated_game.age_range,
            difficulty=updated_game.difficulty,
            creator=str(updated_game.creator.id),
            activities=updated_game.activities,  # Return full activities
            target_range=updated_game.target_range,
            max_time_allowed=updated_game.max_time_allowed,
            total_points=updated_game.total_points,
            template=updated_game.template
        )

    except Exception as e:
        print(f"Error updating game: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{game_id}")
async def delete_game(game_id: str):
    game = await Game.get(validate_object_id(game_id,"game_id"))
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    await game.delete()
    return {"message": "Game deleted successfully"}

@router.patch("/{game_id}/activities", response_model=GameResponse)
async def add_activity_to_game(
    game_id: str = Path(..., description="The ID of the game to update"),
    activities: AddActivities = Body(..., description="Activities to add to the game")
):
    game = await Game.get(validate_object_id(game_id,"game_id"))
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:

        for activity_id in activities.activity_ids:
            activity = await Activity.get(validate_object_id(activity_id,"activity_id"))
            if not activity:
                raise HTTPException(
                    status_code=404,
                    detail="Activity with id {activity_id} not found"
                )
            game.activities.append(activity) 
            await game.update_stats()
        
        await game.save()
        return GameResponse(
            id=str(game.id),
            title=game.title,
            description=game.description,
            age_range=game.age_range,
            difficulty=game.difficulty,
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
    
@router.delete("/{game_id}/activities/{activity_id}", response_model=GameResponse)
async def remove_activity_from_game(
    game_id: str = Path(..., description="The ID of the game to update"),
    activity_id: str = Path(..., description="The ID of the activity to remove")
):
    game = await Game.get(validate_object_id(game_id,"game_id"))
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        # Remove activity from the game's activities list
        game.activities = [activity for activity in game.activities if str(activity.id) != activity_id]
        await game.update_stats()
        await game.save()

        return GameResponse(
            id=str(game.id),
            title=game.title,
            description=game.description,
            age_range=game.age_range,
            difficulty=game.difficulty,
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