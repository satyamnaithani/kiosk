from pydantic import BaseModel
from typing import List

class Answers(BaseModel):
    question_id: int
    option_id: int

class AssessmentSchema(BaseModel):
    assessment: List[Answers]
    training_id: int
