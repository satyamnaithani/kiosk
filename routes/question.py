from fastapi import APIRouter, Depends, HTTPException, Response, status
from config.db import get_db
from models import Training, QuestionOption, TrainingQuestion, TrainingAssignee
from schemas import TrainingQuestionSchema
from sqlmodel import Session
from datetime import date, datetime
from utils import app_service
from utils.oauth2 import oauth2_scheme

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

@question_route.get("/{training_id}")
async def get_questions(training_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    result = db.query(TrainingQuestion).filter(TrainingQuestion.training_id == training_id).all()
    if len(result) == 0:
        return {
            "status": 404,
            "message": "No Questions Found"
        }
    questions = []
    total_marks = 0
    for ques in result:
        options = []
        for op in ques.options:
            options.append({
                "id": op.id,
                "option": op.question_option
            })
        total_marks += int(ques.score)
        questions.append({
            "id": ques.id,
            "question": ques.question,
            "score": int(ques.score),
            "options": options,
        })
    response = {
        "training": ques.training.title,
        "duration_window": ques.training.duration_window,
        "questions": questions,
        "total_marks": total_marks
    }
    return response

@question_route.post("/")
async def write_question(questions: TrainingQuestionSchema, response: Response, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    training_id = questions.training_id
    assigned_training_count = db.query(TrainingAssignee).filter(TrainingAssignee.training_id == training_id).count()
    if assigned_training_count > 0:
        raise HTTPException(status_code=405, detail="Can not assign question to this training. Training already assigned to employee.")
        
    for question in questions.questions:
        x = TrainingQuestion(
            training_id = training_id,
            question = question.question,
            score = question.score,
            status = True,
            created_at = date.today(),
            updated_at = date.today()
        )
        db.add(x)
        db.flush()
        db.refresh(x)
        questions = []
        for question_option in question.options:
            option = QuestionOption(
                question_id = x.id,
                question_option = question_option.question_option,
                is_correct = question_option.is_correct
            )
            questions.append(option)
        db.bulk_save_objects(questions)
    db.commit()
    response.status_code = status.HTTP_201_CREATED

    return { "message": "Question Created Succesfully" }
