from pydantic import BaseModel

class TrainingSchema(BaseModel):
    title: str
    description: str
    status: bool
    min_pass_marks: str
    start_date: int
    end_date: int
    duration_window: int