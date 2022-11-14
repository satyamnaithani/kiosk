from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department
from schemas import EmployeeSchema, DepartmentSchema
from sqlmodel import Session
from datetime import date
from datetime import datetime
from utils import app_service
from utils.oauth2 import oauth2_scheme

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

@department_route.get("/")
async def get_departments(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    departments = db.query(Department).all()
    response = []
    for department in departments:
        response.append({"id": department.id, "name": department.name})
    return response

@department_route.post("/")
async def create_department(payload: DepartmentSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    department = Department(
        name = payload.name,
        status = payload.status,
        hod = payload.hod,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(department)
    db.commit()
    response = {
        status: 201,
        message: "Department Created Succesfully"
    }
    return response