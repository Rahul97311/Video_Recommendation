from fastapi import FastAPI
from app.api.video_routes import router as video_router

app = FastAPI()

app.include_router(video_router, prefix="/videos", tags=["Videos"])