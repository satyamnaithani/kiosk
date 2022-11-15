from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Grievance, Employee
from schemas import GrievanceSchema, GrievanceCloseSchema
from sqlmodel import Session
from datetime import date
from utils import app_service
from utils.oauth2 import oauth2_scheme

grievance_route = APIRouter(
    prefix="/v1/grievances",
    tags=["Grievances"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@grievance_route.get("/")
async def get_grievance(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    employee = db.query(Employee).get(employee_id)
    if employee.type == "admin":
        return db.query(Grievance).all()
    return db.query(Grievance).filter(Grievance.created_by == employee.id).all()


@grievance_route.post("/")
async def create_grievance(grievance: GrievanceSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    x = Grievance(
        title = grievance.title,
        description = grievance.description,
        status = grievance.status,
        remarks = grievance.remarks,
        created_by = employee_id,
        created_at = date.today()
    )
    db.add(x)
    db.commit()
    response = {
        "status": 201,
        "message": "Grievance Created Succesfully"
    }
    return response

@grievance_route.patch("/{grievance_id}")
async def close_grievance(grievance_id:int, grievance: GrievanceCloseSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    update_grievance = {
        Grievance.status: grievance.status,
        Grievance.grievance_feedback: grievance.grievance_feedback,
        Grievance.closed_by: employee_id,
        Grievance.closed_at: date.today()
    }
    db.query(Grievance).filter(Grievance.id == grievance_id).update(update_grievance)
    db.commit()
    response = {
        "status": 200,
        "message": "Grievance Updated Succesfully"
    }
    return response