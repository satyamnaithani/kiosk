from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Hazard, Employee
from schemas import HazardSchema, HazardCloseSchema
from sqlmodel import Session
from datetime import date
from utils import app_service
from utils.oauth2 import oauth2_scheme

hazard_route = APIRouter(
    prefix="/v1/hazards",
    tags=["Hazards"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@hazard_route.get("/")
async def get_hazards(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    employee = db.query(Employee).get(employee_id)
    if employee.type == "admin": 
        return db.query(Hazard).all()
    if employee.is_hod:
        return db.query(Hazard).filter(Hazard.department_id == employee.department_id).all()
    return db.query(Hazard).filter(Hazard.created_by == employee.id).all()


@hazard_route.post("/")
async def create_hazard(hazard: HazardSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    x = Hazard(
        title = hazard.title,
        description = hazard.description,
        type = hazard.type,
        department_id = hazard.department_id,
        status = hazard.status,
        remarks = hazard.remarks,
        created_by = employee_id,
        created_at = date.today()
    )
    db.add(x)
    db.commit()
    response = {
        "status": 201,
        "message": "Hazard Created Succesfully"
    }
    return response

@hazard_route.patch("/{hazard_id}")
async def close_hazard(hazard_id:int, hazard: HazardCloseSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    employee = db.query(Employee).get(employee_id)
    if employee.type != "admin":
        return {
            "status": 405,
            "message": "Updation not allowed. Please login from admin account"
        }
    update_hazard = {
        Hazard.status: hazard.status,
        Hazard.hazard_feedback: hazard.hazard_feedback,
        Hazard.closed_by: employee_id,
        Hazard.closed_at: date.today()
    }
    db.query(Hazard).filter(Hazard.id == hazard_id).update(update_hazard)
    db.commit()
    response = {
        "status": 200,
        "message": "Hazard Updated Succesfully"
    }
    return response