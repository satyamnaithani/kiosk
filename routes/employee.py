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

employee = APIRouter()

@employee.post("/login")
async def login(payload: LoginSchema, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email==payload.email).first()

    if not employee:
        return {"message": "Employee not found"}

    if not app_service.verify_password(payload.password, employee.password):
        return {"message": "invalid credentials!"}
    name = employee.name
    jwt = await app_service.create_token(name)
    response = {
        "employee_code": employee.employee_code,
        "name": name,
        "mobile": employee.mobile,
        "email": employee.email,
        "type": employee.type,
        "jwt": jwt,
    }
    return {"message": response}

@employee.get("/employee")
async def get_employees(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Employee).all()

@employee.post("/employee")
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

@employee.get("/departments")
async def get_departments(token: str, db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    departments = db.query(Department).all()
    response = []
    for department in departments:
        response.append({"id": department.id, "name": department.name})
    return response