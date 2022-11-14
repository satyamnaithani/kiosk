from pydantic import BaseModel

class TrainingSchema(BaseModel):
    title: str
    description: str
    status: bool
    start_date: str
    end_date: str
    duration_window: int