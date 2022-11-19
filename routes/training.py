from fastapi import APIRouter, Depends
from config.db import get_db
from models import Training, QuestionAnswer, TrainingQuestion, QuestionOption, Assesment, TrainingAssignee, Employee
from schemas import TrainingSchema, AssessmentSchema
from sqlmodel import Session
from datetime import datetime, date
from utils import app_service
from utils.oauth2 import oauth2_scheme

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
async def get_trainings(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Training).all()

@training_route.post("/")
async def create_training(payload: TrainingSchema, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    app_service.authMiddleware(token)
    training = Training(
        title = payload.title,
        description = payload.description,
        status = payload.status,
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
async def submit_assessment(payload: AssessmentSchema, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
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
    db.query(TrainingAssignee).filter(TrainingAssignee.employee_id == employee_id, TrainingAssignee.training_id == payload.training_id).update({TrainingAssignee.status: 'completed'})
    db.commit()
    response = {
        "status": 201,
        "message": "Assesment Submitted Succesfully"
    }
    return response

@training_route.get("/assessment/score_card/{training_id}")
async def submit_assessment(training_id: int, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    answer_sheet = db.query(QuestionAnswer.question_id, QuestionAnswer.answer_id).filter(QuestionAnswer.employee_id == employee_id, QuestionAnswer.training_id == training_id).all()
    correct_answers = db.query(TrainingQuestion, QuestionOption.id).filter(QuestionOption.is_correct == 1, TrainingQuestion.training_id == training_id).all()
    response = {
        "status": 200,
        "message": answer_sheet,
        "hehe": correct_answers
    }
    return response

@training_route.get("/results/{employee_id}")
async def fetch_assessment_results(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    assessment_response = []
    assessments = db.query(Assesment).filter(Assesment.employee_id == employee_id).all()
    for assessment in assessments:
        question_answer_response = []
        total_score = 0
        for question_answer in assessment.question_answers:
            option_arr = []
            for option in question_answer.question.options:
                if question_answer.answer_id == option.id:
                    if option.is_correct:
                        total_score += int(question_answer.question.score)
                option_arr.append({
                    "id": option.id,
                    "is_correct": option.is_correct
                })
            question_answer_response.append({
                "question_id": question_answer.question_id,
                "answer_id": question_answer.answer_id,
                "question": {
                    "id": question_answer.question.id,
                    "score": int(question_answer.question.score),
                    "options": option_arr
                }
            })
        assessment_response.append({
            "id": assessment.id,
            "total_score": total_score,
            "question_answers": question_answer_response,
            
        })
    return assessment_response


@training_route.get("/assigned-trainings")
async def assigned_trainings(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    trainings = db.query(TrainingAssignee).filter(Employee.id == employee_id).all()
    if trainings == None:
        response = {
            "status": 404,
            "message": "Trainings Not found"
        }
    else:
        trainings_response = []
        for training in trainings:
            trainings_response.append({
                "id": training.training.id,
                "title": training.training.title,
                "description": training.training.description,
                "status": training.status,
                "start_date": training.training.start_date,
                "end_date": training.training.end_date,
                "duration_window": training.training.duration_window,
                "created_at": training.training.created_at,
                "updated_at": training.training.updated_at
            })
    response = {
        "status": 200,
        "data": trainings_response
    }
    return response
