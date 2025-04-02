from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from motor.motor_asyncio import AsyncIOMotorClient
from app.routers import users, activities, games , badges , progression
from app.models.user import User
from app.models.activity import Activity
from app.models.game import Game
from app.models.badge import Badge
from app.models.progress import Progress
from dotenv import load_dotenv
from beanie import init_beanie
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173",os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(users.router)
app.include_router(activities.router)
app.include_router(games.router)
app.include_router(badges.router)
app.include_router(progression.router)


# Connect to MongoDB
uri = os.getenv("DB_URI")
client = AsyncIOMotorClient(uri)

async def init_db():
    try:
        await init_beanie(
            database=client.get_database("mathtastic"),
            document_models=[User, Activity, Game, Badge, Progress]
        )
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome To MathTastic!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )





