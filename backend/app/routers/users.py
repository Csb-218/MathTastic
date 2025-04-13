import os
from datetime import datetime,timedelta
from fastapi import APIRouter, Depends, HTTPException , Response , Request
from fastapi.security import HTTPBearer
import jwt
from dotenv import load_dotenv
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin 
from app.utils.helpers import verify_token , serialize_user_for_cookie

load_dotenv()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

security = HTTPBearer(
    scheme_name="Bearer",
    description="Enter the Firebase JWT token",
    auto_error=True,
    bearerFormat="JWT"
)

def serialize_datetime(obj):
    """Helper function to serialize datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# get all users
@router.get("/", response_model=list[User])
async def get_users():
    try:
        users = await User.find_all().to_list()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}") from e

# Add new user
@router.post("/register",
            response_model=User,
            summary="User Signup",
            description="Register a new user with Firebase token",
            responses={
                200: {"description": "Successful registration"},
                400: {"description": "Invalid user data"},
                401: {"description": "Invalid authentication credentials"}
            }
            )
async def register_user(user: UserCreate,
                        token_data: dict = Depends(verify_token)):
    try:
        existing_user = await User.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        new_user = User(
            name=user.name,
            email=user.email,
            uid=user.uid,
            role=user.role,
            created_at=datetime.now()
        )
        await new_user.insert()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error registering user: {str(e)}") from e

# login user
@router.post(
    "/login", 
    summary="User Login",
    description="Authenticate user with Firebase token and return user details"
)
async def login_user(
    user_data: UserLogin,
    verified_token: dict = Depends(verify_token)  # Get the verified token data
) :
    try:

        # token_data contains the decoded Firebase token
        if verified_token['token_data']['user_id'] != user_data.uid:
            raise HTTPException(
                status_code=401,
                detail="Token UID does not match provided UID"
            )
        
        # Find user in database
        user = await User.find_one({
            "email": user_data.email,
            "uid": user_data.uid  # Add this check for extra security
        })
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        payload = {
            "exp": datetime.now() + timedelta(seconds=3600),
            "iat": datetime.now(),
            "sub": serialize_user_for_cookie(user)
        }


        token = jwt.encode(
            payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )
        
        return {"message": "Login successful", "token": token}
        

    except Exception as e:
        print (e)
        raise HTTPException(
            status_code=401,
            detail=str(e)
        ) from e

# check user authentication
@router.get(
    "/check-auth",
    summary="Check Authentication",
    description="Check if the user is authenticated using the JWT token"
)
async def check_auth(
    request: Request
):
    try:
        if request.cookies.get("user_cookie") is None:
            raise HTTPException(
                status_code=401,
                detail="No authentication token provided"
            )
        # If the token is valid, return the user data
        return {"message": "User is authenticated"}
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401, 
            detail='Invalid authentication credentials'
        ) from e

