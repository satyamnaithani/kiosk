from fastapi import APIRouter, Depends
from config.db import get_db
from models import Training, QuestionAnswer, TrainingQuestion, QuestionOption, Assesment
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
        start_date = app_service.format_date(payload.start_date),
        end_date = app_service.format_date(payload.end_date),
        duration_window = payload.duration_window,
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
    assessment = Assesment(
        employee_id = employee_id,
        training_id = payload.training_id,
        status = True,
        created_at = date.today()
    )
    db.add(assessment)
    db.flush()

    answers = []
    for ques in payload.assessment:
        question_answer = QuestionAnswer(
            question_id = ques.question_id,
            answer_id = ques.option_id,
            employee_id = employee_id,
            assessment_id = assessment.id
        )
        answers.append(question_answer)
    db.bulk_save_objects(answers)
    db.commit()
    response = {
        "status": 201,
        "message": "Assesment Submitted Succesfully"
    }
    return response

@training_route.get("/assessment/score_card/{training_id}")
async def submit_assessment(token: str, training_id: int, db:Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    answer_sheet = db.query(QuestionAnswer.question_id, QuestionAnswer.answer_id).filter(QuestionAnswer.employee_id == employee_id, QuestionAnswer.training_id == training_id).all()
    correct_answers = db.query(TrainingQuestion, QuestionOption.id).filter(QuestionOption.is_correct == 1, TrainingQuestion.training_id == training_id).all()
    response = {
        "status": 200,
        "message": answer_sheet,
        "hehe": correct_answers
    }
    return response
