from pydantic import BaseModel

class TrainingQuestionSchema(BaseModel):
    training_id: int
    question: str
    score: str
    status: bool