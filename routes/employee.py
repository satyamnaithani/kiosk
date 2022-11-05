from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department
from schemas import EmployeeSchema, LoginSchema, Token
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
async def write_data(token: str, employee: EmployeeSchema, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    x = Employee(
        employee_code = employee.employee_code,
        name = employee.name,
        department_id = employee.department_id,
        mobile = employee.mobile,
        email = employee.email,
        password =app_service.get_password_hash(employee.password),
        type = employee.type,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(x)
    db.commit()
    return {"message": "Employee Created Succesfully"}