from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Request, HTTPException, Header, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.firebase_admin import auth_instance as auth
from typing import Annotated

class JWTBearer(HTTPBearer):
    """
    Security scheme for JWT bearer authentication using Firebase tokens.
    
    Attributes:
        auto_error (bool): Whether to auto-error on missing/invalid token
    """
    def __init__(self):
        super().__init__(
            scheme_name="JWT",
            description="Enter your Firebase JWT token",
            bearerFormat="JWT",
            auto_error=True
        )

# Initialize security scheme with documentation
security = JWTBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Verify Firebase JWT token and return decoded token data.
    
    Args:
        credentials (HTTPAuthorizationCredentials): The bearer token credentials
        
    Returns:
        dict: Decoded token containing user information
        
    Raises:
        HTTPException: If token is invalid or verification fails
    """
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return {"token_data": decoded_token,"token":token}
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def validate_object_id(id_str: str, id_name: str) -> ObjectId:
    """
    Validate and convert string to MongoDB ObjectId.
    
    Args:
        id_str (str): String to convert to ObjectId
        id_name (str): Name of the ID field for error messages
        
    Returns:
        ObjectId: Valid MongoDB ObjectId
        
    Raises:
        HTTPException: If ID format is invalid
    """
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=400, 
            detail=f'Invalid {id_name} ID format'
        )
    

def serialize_user_for_cookie(user):
    """Helper function to serialize user data for cookie"""
    user_dict = user.model_dump()
    # Convert ObjectId to string
    if 'id' in user_dict:
        user_dict['id'] = str(user_dict['id'])
    # Convert datetime to ISO format
    if 'created_at' in user_dict:
        user_dict['created_at'] = user_dict['created_at'].isoformat()
    return user_dict

