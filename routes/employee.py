from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department
from schemas import EmployeeSchema, LoginSchema, Token, EmployeeDeleteSchema
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from datetime import datetime, timedelta
from utils import app_service

employee_route = APIRouter(
    prefix="/v1/employee",
    tags=["Employee"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@employee_route.get("/")
async def get_employees(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Employee).all()

@employee_route.post("/")
async def create_employee(token: str, employee: EmployeeSchema, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    employee_count = db.query(Employee).count()
    name = employee.name
    employee_code = (name[0] + name[len(name) - 1]).upper() + str(1000 + employee_count)
    x = Employee(
        employee_code = employee_code,
        name = name,
        department_id = employee.department_id,
        mobile = employee.mobile,
        email = employee.email,
        password =app_service.get_password_hash(employee.password),
        type = employee.type,
        is_hod = employee.is_hod,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(x)
    db.flush()
    if employee.is_hod: 
        db.query(Department).filter(Department.id == employee.department_id).update({Department.hod: x.id, Department.updated_at: date.today()}, synchronize_session = False)
    db.commit()
    response = {
        "status": 201,
        "message": "Employee Created Succesfully"
    }
    return response

@employee_route.delete("/")
async def delete_employee(token: str, employee_id: EmployeeDeleteSchema, db: Session = Depends(get_db)):
    app_service.authMiddleware((token))
    db.query(Employee).filter_by(Employee.id == employee_id).delete()
    response = {
        "status": 200,
        "message": "Employee Deleted Succesfully"
    }
    return response