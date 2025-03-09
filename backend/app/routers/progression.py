from fastapi import APIRouter, HTTPException, Path, Depends
from typing import List
from beanie import Document, Link
from app.models.progress import Progress
from app.models.user import User
from app.models.activity import Activity
from app.models.game import Game
from app.schemas.progress_schema import ProgressCreate, ProgressUpdate, ProgressResponse
from app.utils.helpers import validate_object_id

router = APIRouter(
    prefix="/progress",
    tags=["progress"],
    responses={404: {"description": "Not found"}}
)


@router.post("/create", response_model=ProgressResponse)
async def create_progress(progress_data: ProgressCreate):
    try:
        print("1. Progress Data Received:", progress_data.model_dump())

        # Verify student exists
        student_id = validate_object_id(progress_data.student_id, "student_id")
        student = await User.get(student_id)
        print("2. Student Found:", bool(student))
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Initialize progress with proper Links
        progress_dict = {
            "student": Link(student, User),  # Store reference only
            "games_completed": [],
            "badges": [],
            "points_earned": progress_data.points_earned or 0,
            "active_game": None,
            "current_game_level": None,
            "active_activity": None
        }
        print("3. Initial Progress Dict:", progress_dict)

        # Handle optional active game and activity
        if progress_data.active_game:
            print("4. Processing Active Game ID:", progress_data.active_game)
            game_id = validate_object_id(progress_data.active_game, "active_game")
            game = await Game.get(game_id)
            print("5. Active Game Found:", bool(game))
            if game:
                progress_dict["active_game"] = Link(game_id, Game)  # Store reference only
                progress_dict["current_game_level"] = progress_data.current_game_level
                print("6. Updated with Game Reference")

        if progress_data.active_activity:
            print("7. Processing Active Activity ID:", progress_data.active_activity)
            activity_id = validate_object_id(progress_data.active_activity, "active_activity")
            activity = await Activity.get(activity_id)
            print("8. Active Activity Found:", bool(activity))
            if activity:
                progress_dict["active_activity"] = Link(activity_id, Activity)  # Store reference only
                print("9. Updated with Activity Reference")

        # Create progress record
        print("10. Creating Progress with Dict:", progress_dict)
        progress = Progress(**progress_dict)
        await progress.insert()
        print("11. Progress Created with ID:", str(progress.id))
        
        # Fetch references for response
        student = await progress.student.fetch()
        active_game = await progress.active_game.fetch() if progress.active_game else None
        active_activity = await progress.active_activity.fetch() if progress.active_activity else None
        
        response = ProgressResponse(
            id=str(progress.id),
            student_id=str(student.id),
            games_completed=[str(game.ref.id) for game in progress.games_completed],
            badges=[str(badge.ref.id) for badge in progress.badges],
            points_earned=progress.points_earned,
            active_game=str(active_game.id) if active_game else None,
            current_game_level=progress.current_game_level,
            active_activity=str(active_activity.id) if active_activity else None
        )
        print("12. Returning Response:", response.model_dump())
        return response

    except Exception as e:
        print("ERROR in create_progress:", str(e))
        print("ERROR type:", type(e).__name__)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{student_id}", response_model=ProgressResponse)
async def get_progress(
    student_id: str = Path(..., description="The ID of the student")
):
    try:
        object_id = validate_object_id(student_id,"student_id")
        progress = await Progress.find_one({"student.id": object_id})
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")
        
        return ProgressResponse(
            id=str(progress.id),
            student_id=str(progress.student.id),
            games_completed=[str(game.id) for game in progress.games_completed],
            badges=[str(badge.id) for badge in progress.badges],
            points_earned=progress.points_earned
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{student_id}/update", response_model=ProgressResponse)
async def update_progress(
    student_id: str = Path(..., description="The ID of the student"),
    progress_update: ProgressUpdate = None
):
    try:
        student_object_id = validate_object_id(student_id, "student_id")
        progress = await Progress.find_one({"student.id": student_object_id})
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")

        # Handle completed game
        if progress_update.game_id:
            game_id = validate_object_id(progress_update.game_id, "game_id")
            game = await Game.get(game_id)
            if not game:
                raise HTTPException(status_code=404, detail="Game not found")
            progress.games_completed.append(Link(game_id, Game))

        # Update active game and level
        if progress_update.active_game:
            game_id = validate_object_id(progress_update.active_game, "active_game")
            game = await Game.get(game_id)
            if not game:
                raise HTTPException(status_code=404, detail="Active game not found")
            progress.active_game = Link(game_id, Game)
            progress.current_game_level = progress_update.current_game_level

        # Update active activity
        if progress_update.active_activity:
            activity_id = validate_object_id(progress_update.active_activity, "active_activity")
            activity = await Activity.get(activity_id)
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            progress.active_activity = Link(activity_id, Activity)

        await progress.save()
        
        # Fetch references for response
        student = await progress.student.fetch()
        active_game = await progress.active_game.fetch() if progress.active_game else None
        active_activity = await progress.active_activity.fetch() if progress.active_activity else None
        
        return ProgressResponse(
            id=str(progress.id),
            student_id=str(student.id),
            games_completed=[str(game.ref.id) for game in progress.games_completed],
            badges=[str(badge.ref.id) for badge in progress.badges],
            points_earned=progress.points_earned,
            active_game=str(active_game.id) if active_game else None,
            current_game_level=progress.current_game_level,
            active_activity=str(active_activity.id) if active_activity else None
        )
    except Exception as e:
        print(f"Error updating progress: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{student_id}")
async def delete_progress(
    student_id: str = Path(..., description="The ID of the student")
):
    try:
        object_id = validate_object_id(student_id,"student_id")
        progress = await Progress.find_one({"student.id": object_id})
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")
        
        await progress.delete()
        return {"message": "Progress deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))