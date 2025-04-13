from contextlib import asynccontextmanager
import os
from fastapi.middleware.cors import CORSMiddleware  
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import users, activities, games , badges 
from app.lib.db import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI app.
    
    This function initializes the database connection when the app starts
    and closes it when the app stops.
    """ 
    await init_db()
    yield
       

app = FastAPI(lifespan=lifespan)
print(os.getenv("FRONTEND_HOST"))
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_HOST")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# routes
app.include_router(users.router)
app.include_router(activities.router)
app.include_router(games.router)
app.include_router(badges.router)

@app.get("/")
async def root():
    return {"message": "Welcome To MathTastic!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        port=os.getenv("PORT") or 8000,
        reload=True
    )





