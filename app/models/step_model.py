from pydantic import BaseModel

class Step(BaseModel):
    step_id: int
    title: str
    instruction: str


class StepRequest(BaseModel):
    step: Step
    device_os: str