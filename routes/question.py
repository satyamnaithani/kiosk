from fastapi import APIRouter, Depends
from config.db import get_db
from models import Training, QuestionOption
from schemas import TrainingQuestionSchema
from sqlmodel import Session
from datetime import date, datetime
from utils import app_service

question_route = APIRouter(
    prefix="/v1/questions",
    tags=["Questions"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@question_route.post("/")
async def write_question(token: str, questions: TrainingQuestionSchema, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    for question in questions.questions:
        x = TrainingQuestion(
            training_id = questions.training_id,
            question = question.question,
            score = question.score,
            status = question.status,
            created_at = date.today(),
            updated_at = date.today()
        )
        db.add(x)
        db.flush()
        db.refresh(x)
        for question_option in question.options:
            option = QuestionOption(
                question_id = x.id,
                question_option = question_option.question_option,
                is_correct = question_option.is_correct
            )
        db.add(option)
    db.commit()
    return {"message": "Question Created Succesfully"}