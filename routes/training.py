from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Training, QuestionOption
from schemas import TrainingQuestionSchema, TrainingSchema
from sqlmodel import Session
from datetime import date
from jose import JWTError, jwt
from datetime import datetime
from utils import app_service

training = APIRouter()

@training.get("/trainings")
async def get_trainings(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Training).all()

@training.post("/training")
async def create_training(token: str, payload: TrainingSchema, db:Session = Depends(get_db)):
    app_service.authMiddleware(token)
    training = Training(
        title = payload.title,
        description = payload.description,
        status = payload.status,
        min_pass_marks = payload.min_pass_marks,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(training)
    db.commit()
    return {"message": "Training Created Succesfully"}

@training.post("/questions")
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
