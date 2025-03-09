from fastapi import APIRouter, HTTPException, Path
from app.models.activity import Activity
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate, ActivityResponse
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from app.utils.helpers import validate_object_id

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ActivityResponse])
async def get_activities():
    try:
        activities = await Activity.find_all().to_list()
        return [
            ActivityResponse(
                id=str(activity.id),  # Convert ObjectId to string
                level=activity.level,
                target=activity.target,
                addends=activity.addends,
                addends_size=activity.addends_size,
                time_limit=activity.time_limit,
                hints=activity.hints,
                points=activity.points,
                success_feedback=activity.success_feedback,
                failure_feedback=activity.failure_feedback
            ) 
            for activity in activities
        ]
    except Exception as e:
        print(f"Error retrieving activities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: str = Path(..., description="The ID of the activity to get")
):

    activity = await Activity.get(validate_object_id(activity_id,"activity_id"))
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return ActivityResponse(
        id=str(activity.id),
        level=activity.level,
        target=activity.target,
        addends=activity.addends,
        addends_size=activity.addends_size,
        time_limit=activity.time_limit,
        hints=activity.hints,
        points=activity.points,
        success_feedback=activity.success_feedback,
        failure_feedback=activity.failure_feedback
    )

@router.post("/create", response_model=ActivityResponse)
async def create_activity(activity: ActivityCreate):
    try:
        new_activity = Activity(**activity.model_dump())
        await new_activity.insert()
        
        # Convert the response to ActivityResponse format
        return ActivityResponse(
            id=str(new_activity.id),  # Convert ObjectId to string
            level=new_activity.level,
            target=new_activity.target,
            addends=new_activity.addends,
            addends_size=new_activity.addends_size,
            time_limit=new_activity.time_limit,
            hints=new_activity.hints,
            points=new_activity.points,
            success_feedback=new_activity.success_feedback,
            failure_feedback=new_activity.failure_feedback
        )
    except Exception as e:
        print(f"Error creating activity: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{activity_id}/update", response_model=ActivityResponse)
async def update_activity(
    activity_id: str = Path(..., description="The ID of the activity to update"),
    activity_update: ActivityUpdate = None
):
    try:
        activity = await Activity.get(validate_object_id(activity_id,"activity_id"))
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        update_data = activity_update.model_dump(exclude_unset=True)
        if update_data:
            await activity.update({"$set": update_data})
            # Fetch the updated activity
            activity = await Activity.get(object_id)
        
        # Convert the response to ActivityResponse format
        return ActivityResponse(
            id=str(activity.id),
            level=activity.level,
            target=activity.target,
            addends=activity.addends,
            addends_size=activity.addends_size,
            time_limit=activity.time_limit,
            hints=activity.hints,
            points=activity.points,
            success_feedback=activity.success_feedback,
            failure_feedback=activity.failure_feedback
        )
    except Exception as e:
        print(f"Error updating activity: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: str = Path(..., description="The ID of the activity to delete")
):
    activity = await Activity.get(validate_object_id(activity_id,"activity_id"))
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    await activity.delete()
    return {"message": "Activity deleted successfully"}