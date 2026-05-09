from fastapi import APIRouter
from app.models.step_model import StepRequest
from app.services.youtube_service import get_best_videos

router = APIRouter()

@router.post("/step")
def get_step_videos(request: StepRequest):
    step = request.step.dict()
    device_os = request.device_os

    videos = get_best_videos(step, device_os)

    return {
        "step_id": step["step_id"],
        "videos": videos
    }