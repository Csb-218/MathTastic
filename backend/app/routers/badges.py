from fastapi import APIRouter, HTTPException, Path
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from app.models.badge import Badge
from app.schemas.badge_schema import BadgeCreate, BadgeUpdate, BadgeResponse

router = APIRouter(
    prefix="/badges",
    tags=["badges"],
    responses={404: {"description": "Not found"}}
)

def validate_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid badge ID format")

@router.post("/create", response_model=BadgeResponse)
async def create_badge(badge: BadgeCreate):
    try:
        new_badge = Badge(**badge.model_dump())
        await new_badge.insert()
        return BadgeResponse(
            id=str(new_badge.id),
            badge_name=new_badge.badge_name,
            points_to_badge=new_badge.points_to_badge
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BadgeResponse])
async def get_badges():
    try:
        badges = await Badge.find_all().to_list()
        return [
            BadgeResponse(
                id=str(badge.id),
                badge_name=badge.badge_name,
                points_to_badge=badge.points_to_badge
            )
            for badge in badges
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{badge_id}", response_model=BadgeResponse)
async def get_badge(badge_id: str = Path(..., description="The ID of the badge to get")):
    try:
        object_id = validate_object_id(badge_id)
        badge = await Badge.get(object_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        return BadgeResponse(
            id=str(badge.id),
            badge_name=badge.badge_name,
            points_to_badge=badge.points_to_badge
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{badge_id}/update", response_model=BadgeResponse)
async def update_badge(
    badge_id: str = Path(..., description="The ID of the badge to update"),
    badge_update: BadgeUpdate = None
):
    try:
        object_id = validate_object_id(badge_id)
        badge = await Badge.get(object_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        
        await badge.update({"$set": badge_update.model_dump()})
        updated_badge = await Badge.get(object_id)
        return BadgeResponse(
            id=str(updated_badge.id),
            badge_name=updated_badge.badge_name,
            points_to_badge=updated_badge.points_to_badge
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{badge_id}")
async def delete_badge(badge_id: str = Path(..., description="The ID of the badge to delete")):
    try:
        object_id = validate_object_id(badge_id)
        badge = await Badge.get(object_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        await badge.delete()
        return {"message": "Badge deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))