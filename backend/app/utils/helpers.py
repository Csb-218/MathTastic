from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
# Helper function to validate ObjectId
def validate_object_id(id_str: str,id_name:str) -> ObjectId:
    try:
        print("id_str:",id_str)
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f'Invalid {id_name} ID format')