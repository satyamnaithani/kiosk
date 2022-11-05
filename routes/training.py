from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import TrainingQuestion
from schemas import TrainingQuestionSchema
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

@training.get("/questions")
async def get_questions(token: str, db: Session = Depends(get_db)):
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

    return db.query(TrainingQuestion).all()

@training.post("/question")
async def write_question(question: TrainingQuestionSchema, db: Session = Depends(get_db)):
    x = TrainingQuestion(
        training_id = question.training_id,
        question = question.question,
        score = question.score,
        status = question.status,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(x)
    db.commit()
    return {"message": "Question Created Succesfully"}

   