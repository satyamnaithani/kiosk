from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Training, QuestionOption
from schemas import TrainingQuestionSchema, TrainingSchema
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from datetime import datetime, timedelta
from utils import app_service

training = APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
def authMiddleware(token, SECRET_KEY, ALGORITHM):
    try:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

@training.get("/trainings")
async def get_trainings(token: str, db: Session = Depends(get_db)):
    authMiddleware(token, SECRET_KEY, ALGORITHM)
    return db.query(Training).all()

@training.post("/training")
async def create_training(token: str, payload: TrainingSchema, db:Session = Depends(get_db)):
    authMiddleware(token, SECRET_KEY, ALGORITHM)
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
async def write_question(questions: TrainingQuestionSchema, db: Session = Depends(get_db)):
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

   