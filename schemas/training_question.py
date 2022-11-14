from pydantic import BaseModel
from typing import List

class Options(BaseModel):
    question_option: str
    is_correct: bool

class Questions(BaseModel):
    question: str
    score: str
    options: List[Options]

class TrainingQuestionSchema(BaseModel):
    training_id: int
    questions: List[Questions]
