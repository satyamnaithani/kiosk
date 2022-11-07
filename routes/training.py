from fastapi import APIRouter, Depends
from config.db import get_db
from models import Training, QuestionAnswer
from schemas import TrainingSchema, AssessmentSchema
from sqlmodel import Session
from datetime import datetime, date
from utils import app_service

training_route = APIRouter(
    prefix="/v1/trainings",
    tags=["Trainings"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@training_route.get("/")
async def get_trainings(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Training).all()

@training_route.post("/")
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
    response = {
        "status": 201,
        "message": "Training Created Succesfully"
    }
    return response

@training_route.post("/assessment")
async def submit_assessment(token: str, payload: AssessmentSchema, db:Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    assessment = []
    for ques in payload.assessment:
        question_answer = QuestionAnswer(
            question_id = ques.question_id,
            answer_id = ques.option_id,
            employee_id = employee_id,
            created_at = date.today()
        )
        assessment.append(question_answer)
    db.bulk_save_objects(assessment)
    db.commit()
    response = {
        "status": 201,
        "message": "Assesment Submitted Succesfully"
    }
    return response
