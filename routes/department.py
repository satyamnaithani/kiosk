from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department
from schemas import EmployeeSchema
from sqlmodel import Session
from datetime import date
from datetime import datetime
from utils import app_service

department_route = APIRouter(
    prefix="/v1/departments",
    tags=["Department"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@department_route.get("/departments")
async def get_departments(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    departments = db.query(Department).all()
    response = []
    for department in departments:
        response.append({"id": department.id, "name": department.name})
    return response