from pydantic import BaseModel

class TrainingSchema(BaseModel):
    title: str
    description: str
    status: bool
    min_pass_marks: str
    start_date: str
    end_date: str
    duration_window: int