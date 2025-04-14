import os
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from app.models.activity import Activity
from app.models.game import Game
from app.models.badge import Badge


load_dotenv()


# Connect to MongoDB
uri = os.getenv("DB_URI")
client = AsyncIOMotorClient(uri)
async def init_db():
    try:
        await init_beanie(
            database=client.get_database("mathtastic"),
            document_models=[User, Activity, Game, Badge]
        )
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e
    
async def close_db():
    try:
        await client.close()
        print("Database connection closed successfully!")
    except Exception as e:
        print(f"Error closing database: {e}")
        raise e